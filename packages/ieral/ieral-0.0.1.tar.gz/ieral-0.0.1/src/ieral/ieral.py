import warnings
import numpy as np
from eral.eral_score import eral_score_with_normalization
from eral.time_series_helpers import _remove_nan_padding_single
from eral.time_series_alignment import sync_n_series_to_prototype, get_score_and_shift
from .noise_estimation import variance_of_diff

class Cluster:
    """ Class representing a cluster in the evolving time series clustering

    The cluster is represented by two structures:
    - PSV (Prototype Shape Vector), which carries the shape of the prototype, representing the shapes of all samples used in
        updating the prototype
    - PCV (Prototype Confidence Vector), which describes how many input samples were used in conditioning the prototype at each
        time point

    The final prototype is obtained by combining PSV and PCV. The prototype is
    only defined in the time points where the PCV is greater than some user-defined threshold, for
    example 0.8 indicating that the prototype is defined at indices where at least 80% of the samples were used in
    conditioning the prototype.

    """

    psv: np.ndarray
    pcv: np.ndarray
    pdv: np.ndarray
    pdv_m2: np.ndarray
    pdv_m2_count: np.ndarray
    number_of_points: int
    initial_std: float
    initial_std_count: int
    alpha: float
    id: int
    eral_exclusion_zone: float = 0.2

    def __init__(self, sample: np.ndarray, id: int,  alpha: float = 0.1, exclusion_zone: float = 0.2, prior_std_band_weight: int = 1, prior_std: float|str = "variance_of_diff"):
        """ Initialize the cluster with a sample.

        Choosing :param:`alpha`: 1.0 --> only use region where all samples were used, results in a short prototype, 
        0.0 --> use all samples, results in a long prototype

        :param sample: Sample to be used as the prototype
        :param alpha: Threshold for the PCV: required proportion of samples to be used in conditioning the prototype.
        :param exclusion_zone: Exclusion zone for the alignment of the new sample to the prototype
        """

        self.psv = sample
        self.pcv = np.ones_like(sample)
        if prior_std_band_weight <= 0:
            self.pdv_m2 = np.zeros_like(sample)
            self.pdv_m2_count = np.ones_like(sample)
            self.initial_std = 0
            self.initial_std_count = 0
        else:
            match prior_std:
                case "variance_of_diff":
                    sample_std = variance_of_diff(sample)
                case _:
                    if type(prior_std) is float:
                        sample_std = prior_std
                    else:
                        raise ValueError("prior_std should be either 'variance_of_diff' or a float")
            self.initial_std = sample_std
            self.pdv_m2 = np.full_like(sample, prior_std_band_weight * (sample_std**2))
            self.pdv_m2_count = np.zeros_like(sample) + prior_std_band_weight
            self.initial_std_count = prior_std_band_weight
        self.number_of_points = 1
        self.alpha = alpha
        self.id = id
        self.eral_exclusion_zone = exclusion_zone

    def try_add_sample(self, sample: np.ndarray, min_new_length: float = 0.8) -> bool:
        """ Try to add a new sample to the cluster

        The new sample is added to the cluster, if the new prototype would not be less than `min_new_length` times
        the length of the old prototype. If the new prototype would be too short, the sample is not added.

        If the sample is added, the prototype is updated, and the number of points is increased. True is returned.
        If the sample is not added, False is returned.

        :param sample: New sample to be added to the cluster
        :param min_new_length: Minimum length of the new prototype as a proportion of the old prototype
        :return: True if the sample was added, False if the sample was not added
        """

        if self.number_of_points == 0:
            raise ValueError("Cluster is not initialized, can not add samples")

        if min_new_length > 1:
            raise ValueError("min_new_length should be less than 1")
        
        new_psv, new_pcv, new_pdv_m2, new_pdv_m2_count, common_time = self._get_new_components(sample)

        start_idx, end_idx = self._calculate_crisp_prototype_boundaries(new_psv, new_pcv, self.alpha)
        new_prototype = new_psv[start_idx:end_idx]

        if len(new_prototype) / len(self.prototype) < min_new_length:
            return False

        self.psv = new_psv
        self.pcv = new_pcv
        self.number_of_points += 1
        # self.common_time = common_time
        self.pdv_m2 = new_pdv_m2
        self.pdv_m2_count = new_pdv_m2_count

        return True

    def _get_alignment_of_sample_to_psv(self, sample: np.ndarray) -> int:
        """ Get the lag to be applied to the sample to align it to the PSV

        Using the crisp prototype, the lag is calculated. Then this lag is modified so that it can be applied to align the sample and the
        PSV.

        The sample must not be simply applied to the PSV, since the PSV contains
        ill-defined values at the edges.

        Attention: "Apply zero mean" is set to False in the call to :func:`eral.time_series_alignment.get_score_and_shift`.

        :param sample: Sample to be aligned to the prototype
        :return: Lag suitable to be applied to the sample to align it to the PSV
        """

        # Get current crisp prototype
        start_idx, end_idx = self._get_crisp_prototype_boundaries()
        prototype = self.psv[start_idx:end_idx]

        # Get optimal alignment of the new sample to the crisp prototype
        alignment: int = get_score_and_shift(prototype, sample, exclusion_zone=self.eral_exclusion_zone, apply_zero_mean=False)[1] # TODO: apply zero mean is fixed, check if it should be changed

        return alignment + start_idx

    def _get_shifted_sample_and_psv_with_alignment(self, sample: np.ndarray) -> tuple[np.ndarray, np.ndarray, int, np.ndarray]:
        """ Shift the sample and the PSV to align them

        Only the crisp prototype is used in the alignment. The PSV is then shifted to match the
        alignment of the sample and the crisp prototype.

        :param sample: Sample to be aligned to the prototype
        :return: Tuple of the shifted sample, the shifted PSV, alignment and common time points
        """

        alignment: int = self._get_alignment_of_sample_to_psv(sample)

        # Use obtained optimal alignment to shift the PSV
        psv = self.psv
        common_time, shifted_samples, shifted_psv = sync_n_series_to_prototype(prototype=psv,
                                                                               series=[sample],
                                                                               shifts=[alignment])
        
        return shifted_samples[0], shifted_psv, alignment, common_time
    

    def _get_shifted_sample_and_psv(self, sample: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """ Shift the sample and the PSV to align them 
        
        Only the crisp prototype is used in the alignment. The PSV is then shifted to match the
        alignment of the sample and the crisp prototype.

        :param sample: Sample to be aligned to the prototype
        :return: Tuple of the shifted sample and the shifted PSV
        """

        shifted_sample, shifted_psv, _, _ = self._get_shifted_sample_and_psv_with_alignment(sample)
        
        return shifted_sample, shifted_psv


    def _generate_new_pcv(self, start_idx: int, end_idx: int) -> np.ndarray:
        """ Generate a new PCV when adding new sample to the cluster 
        
        The region where the new sample is added to the cluster has increased support after the addition. The
        PCV is updated to reflect this change.

        :param start_idx: Start index of the new sample in the PSV
        :param end_idx: End index of the new sample in the PSV
        :return: New PCV
        """

        previous_number_of_points = self.number_of_points
        new_number_of_points = previous_number_of_points + 1

        old_pcv = self.pcv
        new_pcv = old_pcv.copy() * previous_number_of_points
        if start_idx < 0:
            new_pcv = np.concatenate([np.zeros(-start_idx), new_pcv])
            end_idx+=-start_idx
            start_idx = 0
        if end_idx > len(new_pcv):
            new_pcv = np.concatenate([new_pcv, np.zeros(end_idx - len(new_pcv))])
            end_idx = len(new_pcv)

        new_pcv[start_idx:end_idx] += 1

        new_pcv /= new_number_of_points

        return new_pcv

    def _generate_new_psv(self, aligned_sample: np.ndarray, aligned_psv: np.ndarray, aligned_new_pcv: np.ndarray) -> np.ndarray:
        """ Generate a new PSV by adding the new aligned sample to the existing PSV """

        assert len(aligned_sample) == len(aligned_psv), ("Aligned sample and aligned PSV should have the same length. "
                                                                        f"Lengths are {len(aligned_sample)} and "
                                                                        f"{len(aligned_psv)}")
        
        if aligned_new_pcv is None:
            # # Calculate the weights
            # weight_new_sample = 1 / (self.number_of_points + 1)
            # weight_old_prototype = self.number_of_points / (self.number_of_points + 1)

            # # Calculate the new prototype
            # aligned_psv_nan_mask = np.isnan(aligned_psv)
            # aligned_sample_nan_mask = np.isnan(aligned_sample)

            # sample_weights_vector = np.zeros_like(aligned_sample)+weight_new_sample
            # prototype_weights_vector = np.zeros_like(aligned_psv)+weight_old_prototype
            
            # # Weights should be weight_new_sample and weight_old_prototype where neither of the values is NaN
            # pass

            # # At regions where only the sample is NaN, the prototype should be used
            # sample_weights_vector[aligned_sample_nan_mask] = 0
            # prototype_weights_vector[aligned_sample_nan_mask] = 1

            # # At regions where only the prototype is NaN, the sample should be used
            # sample_weights_vector[aligned_psv_nan_mask] = 1
            # prototype_weights_vector[aligned_psv_nan_mask] = 0
            raise ValueError("aligned_new_pcv should not be None")
        else:
            assert len(aligned_new_pcv) == len(aligned_psv), ("Aligned new PCV and aligned PSV should have the same length. "
                                                                        f"Lengths are {len(aligned_new_pcv)} and "
                                                                        f"{len(aligned_psv)}")
            assert np.count_nonzero(np.isnan(aligned_new_pcv)) == 0, ("New PCV should not have NaN values")
            old_number_of_points = self.number_of_points
            new_number_of_points = old_number_of_points + 1
            
            aligned_new_point_count = aligned_new_pcv * new_number_of_points
            sample_nan_mask = np.isnan(aligned_sample)
            aligned_old_point_count = aligned_new_point_count - np.bitwise_not(sample_nan_mask)

            sample_weights_vector = np.bitwise_not(sample_nan_mask) / aligned_new_point_count
            prototype_weights_vector = aligned_old_point_count / aligned_new_point_count

        # The sum of the weights should be 1
        assert np.allclose(sample_weights_vector+prototype_weights_vector, 1), ("Sample and prototype weights should sum to 1")

        weighted_new_sample = aligned_sample * sample_weights_vector
        weighted_old_prototype = aligned_psv * prototype_weights_vector

        new_prototype = np.nansum(np.array([weighted_old_prototype, weighted_new_sample]), axis=0)
        
        return new_prototype


    def _generate_new_m2(self, aligned_sample: np.ndarray, aligned_new_psv: np.ndarray, aligned_old_psv: np.ndarray, aligned_old_m2: np.ndarray) -> np.ndarray:
        """ Generate a new m2 used in new Prototype Deviation Vector """
        start_idx, end_idx = self._get_start_and_end_from_aligned_sample(aligned_sample)

        new_m2 = aligned_old_m2.copy()
        old_m2_nan_mask = np.isnan(aligned_old_m2) # This mask shows where the PSV, M2, PDV have expanded since the last update
        new_m2[old_m2_nan_mask] = 0 # This line sets the value of the new M2 to the initial std where the old M2 is NaN (i.e. where the PSV has just expanded)
        assert np.count_nonzero(np.isnan(aligned_new_psv)) == 0, ("New PSV should not have NaN values")
        aligned_old_psv_nan_mask = np.isnan(aligned_old_psv)
        assert np.equal(aligned_old_psv_nan_mask, old_m2_nan_mask).all(), ("Old PSV and old M2 should have the same NaN values")
        aligned_old_psv_copy = aligned_old_psv.copy()
        aligned_old_psv_copy[aligned_old_psv_nan_mask] = 0 # This will result in new M2 having the value of 0 where the old PSV is NaN (i.e. where the PSV has just expanded)
        new_m2[start_idx:end_idx] += (aligned_sample[start_idx:end_idx] - aligned_new_psv[start_idx:end_idx])*(aligned_sample[start_idx:end_idx] - aligned_old_psv_copy[start_idx:end_idx])
        new_m2[old_m2_nan_mask] = self.initial_std_count * self.initial_std**2 # This is here just for testing purposes, remove it if you see it later on
        assert np.count_nonzero(np.isnan(new_m2)) == 0, ("New m2 should not have NaN values")
        return new_m2
    
    
    # def _generate_new_pdv(self, aligned_new_pcv: np.ndarray, new_m2: np.ndarray) -> np.ndarray:
    #     new_number_of_points = self.number_of_points + 1
    #     aligned_new_point_count = aligned_new_pcv * new_number_of_points

    #     new_pdv = np.sqrt(new_m2 / aligned_new_point_count)
    #     return new_pdv
    def _generate_new_pdv(self, aligned_new_pdv_m2_count: np.ndarray, new_m2: np.ndarray) -> np.ndarray:
        new_pdv = np.sqrt(new_m2 / aligned_new_pdv_m2_count)
        new_pdv = np.nan_to_num(new_pdv, nan=0)
        return new_pdv
    
    def _get_expanded_pdv_m2_count(self, aligned_psv: np.ndarray) -> np.ndarray:
        """ Get the expanded PDV M2 count vector, expanded the same way as PSV and PCV """
        # aligned sample: -----XXXXXXXXX
        # aligned PSV:    XXXXXXXXXX----
        # old M2:         XXXXXXXXXX    
        # new M2:         XXXXXXXXXX----

        assert len(aligned_psv) >= len(self.pdv_m2_count), ("Aligned PSV should be at least as long as the old M2 count")
        new_m2_count: np.ndarray = np.full_like(aligned_psv, np.nan)
        mask: np.ndarray = np.isnan(aligned_psv)
        old_m2_count = self.pdv_m2_count
        assert np.count_nonzero(np.bitwise_not(mask)) == len(old_m2_count)
        new_m2_count[np.bitwise_not(mask)] = old_m2_count
        return new_m2_count

    @property
    def pdv(self) -> np.ndarray:
        """ Get the Prototype Deviation Vector """
        return self._generate_new_pdv(self.pdv_m2_count, self.pdv_m2)

    @property
    def crisp_pdv(self) -> np.ndarray:
        """ Get the Crisp Prototype Deviation Vector """
        start, end = self._get_crisp_prototype_boundaries()
        return self.pdv[start:end]

    @staticmethod
    def _get_start_and_end_from_aligned_sample(aligned_sample: np.ndarray) -> tuple[int, int]:
        """ Given an aligned sample, get the start and end index of the new sample in the PSV

        The aligned sample is assumed to start and/or end with NaN values. The start and end index of the new sample
        are found by counting the number of NaN values at the start and end of the aligned sample.

        :param aligned_sample: Aligned sample
        :return: Tuple of the start and end index of the new sample in the PSV
        """

        start_idx = np.argmax(~np.isnan(aligned_sample))
        end_idx = len(aligned_sample) - np.argmax(~np.isnan(aligned_sample[::-1]))

        return start_idx, end_idx


    def _get_new_components(self, sample: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """ Get the new PSV, the new PCV, and the common time points
        
        The new sample is aligned to the existing crisp prototype. The lag is used to align the sample and the
        PSV. The PSV is then updated by adding the new sample to the prototype.

        The PCV is updated to reflect the latest update.

        This method does not update the cluster, only calculates the new components.

        :param sample: New sample to be added to the cluster
        :return: Tuple of the new PSV, the new PCV, the new PDV M2, and the common time points
        """

        shifted_sample, shifted_psv, alignment, common_time = self._get_shifted_sample_and_psv_with_alignment(sample)
        assert len(shifted_sample) == len(shifted_psv), ("Shifted sample and shifted PSV should have the same length. "
                                                                        f"Lengths are {len(shifted_sample)} and "
                                                                        f"{len(shifted_psv)}")

        new_pcv = self._generate_new_pcv(start_idx=alignment, end_idx=alignment+len(sample))

        new_psv = self._generate_new_psv(shifted_sample, shifted_psv, new_pcv)

        assert len(new_psv) == len(new_pcv), ("New PSV and new PCV should have the same length. "
                                                                            f"Lengths are {len(new_psv)} and "
                                                                            f"{len(new_pcv)}")
        
        aligned_old_m2 = self._get_expanded_m2(shifted_psv)

        new_pdv_m2 = self._generate_new_m2(aligned_sample=shifted_sample,
                                           aligned_new_psv=new_psv,
                                           aligned_old_psv=shifted_psv,
                                           aligned_old_m2=aligned_old_m2)
        
        assert len(new_pdv_m2) == len(new_pcv), ("New M2 and new PCV should have the same length. "
                                                                            f"Lengths are {len(new_pdv_m2)} and "
                                                                            f"{len(new_pcv)}")
        
        new_pdv_m2_count = self._get_expanded_pdv_m2_count(shifted_psv)
        # assert np.count_nonzero(np.isnan(new_pdv_m2_count)) == 0, ("New PDV M2 count should not have NaN values")
        assert len(new_pdv_m2_count) == len(shifted_sample), ("New PDV M2 count and shifted sample should have the same length. "
                                                                            f"Lengths are {len(new_pdv_m2_count)} and "
                                                                            f"{len(shifted_sample)}")
        new_pdv_m2_count[np.isnan(new_pdv_m2_count)] = self.initial_std_count # 0 # This line sets the value of the new PDV M2 count to initial value where the PSV has just expanded
        new_pdv_m2_count[np.bitwise_not(np.isnan(shifted_sample))] += 1

        return new_psv, new_pcv, new_pdv_m2, new_pdv_m2_count, common_time

    def _get_expanded_m2(self, aligned_psv: np.ndarray) -> np.ndarray:
        """ Returns the M2 vector, expanded in the same way as PSV and PCV"""
        
        # aligned sample: -----XXXXXXXXX
        # aligned PSV:    XXXXXXXXXX----
        # old M2:         XXXXXXXXXX    
        # new M2:         XXXXXXXXXX----

        assert len(aligned_psv) >= len(self.pdv_m2), ("Aligned PSV should be at least as long as the old M2")
        new_m2: np.ndarray = np.full_like(aligned_psv, np.nan)
        mask: np.ndarray = np.isnan(aligned_psv)
        old_m2 = self.pdv_m2
        assert np.count_nonzero(np.bitwise_not(mask)) == len(old_m2)
        new_m2[np.bitwise_not(mask)] = old_m2
        return new_m2
        

    def add_sample(self, sample: np.ndarray):
        """ Add a new sample to the cluster

        The new sample is aligned to the existing crisp prototype. The lag is used to align the sample and the
        PSV. The PSV is then updated by adding the new sample to the prototype.

        The PCV is updated to reflect the latest update.

        :param sample: New sample to be added to the cluster
        :return: None
        """

        new_psv, new_pcv, new_m2, new_pdv_m2_count, common_time = self._get_new_components(sample)
        assert len(new_psv) == len(new_pcv) == len(new_m2) == len(new_pdv_m2_count), ("New PSV, new PCV, new M2, and new PDV M2 count should have the same length. ")

        # self.common_time = common_time
        self.psv = new_psv
        self.pcv = new_pcv
        self.number_of_points += 1
        self.pdv_m2 = new_m2
        self.pdv_m2_count = new_pdv_m2_count

    @staticmethod
    def distance(prototype: np.ndarray, sample: np.ndarray, eral_exclusion_zone: float) -> float:
        """ Calculate the distance between the prototype and the sample

        ERAL score with normalization is used to calculate the error in alignment of the sample to the prototype.
        Normalization in ERAL score is done by the length of the overlap of the sample and the prototype.

        ERAL score is further multiplied by (len_sample*len_prototype)/(overlap_len^2) to penalize short overlaps.

        :param prototype: Prototype to be compared to the sample
        :param sample: Sample to be compared to the prototype
        :param eral_exclusion_zone: Exclusion zone for the alignment of the new sample to the prototype
        :return: Distance
        """

        a = _remove_nan_padding_single(prototype)
        b = _remove_nan_padding_single(sample)
        eral_score, normalization = eral_score_with_normalization(a, b)

        if eral_exclusion_zone > 0:
            # Exclude the forbidden shifts
            exclusion_zone = int(len(eral_score) * eral_exclusion_zone)
            eral_score[:exclusion_zone] = np.inf
            eral_score[-exclusion_zone:] = np.inf

        eral_dist = np.min(eral_score)
        normalization = normalization[np.argmin(eral_score)]

        overlap_len = normalization ** 2

        prototype_len = len(_remove_nan_padding_single(prototype))
        sample_len = len(_remove_nan_padding_single(sample))
        factor = (prototype_len * sample_len) / (overlap_len ** 2)

        return eral_dist * normalization * (factor ** 2)
    
    @staticmethod
    def find_subarray_indices(full: np.ndarray, subarray: np.ndarray) -> tuple[int, int]:
        """Find the start and stop indices of the second array within the first array."""
        full_str = ','.join(map(str, full))
        subarray_str = ','.join(map(str, subarray))
        
        start_idx = full_str.find(subarray_str)
        if start_idx == -1:
            raise ValueError("Second array is not a subset of the first array")
        
        start = full_str[:start_idx].count(',')
        stop = start + len(subarray)
        
        return start, stop


    @staticmethod
    def _interval_distance_with_given_alignment(sample: np.ndarray, psv: np.ndarray, prototype_band: np.ndarray, total_alignment: int, prototype_in_psv) -> float:
        
        assert len(psv) == len(prototype_band), ("PSV and prototype band should have the same length")

        _, shifted_samples, shifted_psv = sync_n_series_to_prototype(prototype=psv,
                                                                     series=[sample],
                                                                     shifts=[total_alignment])
        
        _, _, shifted_prototype_band = sync_n_series_to_prototype(prototype=prototype_band,
                                                                  series=[sample],
                                                                  shifts=[total_alignment])

        shifted_sample = shifted_samples[0]
        assert len(shifted_sample) == len(shifted_psv), ("Shifted sample and shifted PSV should have the same length")
        assert len(shifted_psv) == len(shifted_prototype_band), ("Shifted PSV and prototype band should have the same length")

        # Count samples in the prototype band
        upper_band_limit = shifted_psv + shifted_prototype_band
        lower_band_limit = shifted_psv - shifted_prototype_band
        sample_in_band_mask = np.bitwise_and(shifted_sample <= upper_band_limit, shifted_sample >= lower_band_limit)
        # sample_in_band_mask = np.nan_to_num(sample_in_band_mask, nan=False) # NaNs are present where the sample is nan

        proportion_of_samples_in_band = np.count_nonzero(sample_in_band_mask) / len(sample)

        prototype_len = len(_remove_nan_padding_single(prototype_in_psv))
        sample_len = len(_remove_nan_padding_single(sample))
        overlap_len = np.count_nonzero(sample_in_band_mask)
        if overlap_len == 0:
            return np.inf
        else:
            factor = (prototype_len * sample_len) / (np.count_nonzero(sample_in_band_mask) ** 2)
            return (1 - proportion_of_samples_in_band) * (factor)**2
        
    @staticmethod
    def interval_distance(prototype: np.ndarray, sample: np.ndarray, psv: np.ndarray, eral_exclusion_zone: float, prototype_band: np.ndarray) -> float:
        start_idx, end_idx = Cluster.find_subarray_indices(psv, prototype)
        
        # Get optimal alignment of the new sample to the crisp prototype
        alignment: int = get_score_and_shift(prototype, sample, exclusion_zone=eral_exclusion_zone, apply_zero_mean=False)[1] # TODO: apply zero mean is fixed, check if it should be changed

        total_alignment =  alignment + start_idx
        assert len(psv) == len(prototype_band), ("PSV and prototype band should have the same length")

        prototype_in_psv = np.full_like(psv, np.nan)
        prototype_in_psv[start_idx:end_idx] = prototype

        # return Cluster._interval_distance_with_given_alignment(sample, prototype_in_psv, prototype_band, total_alignment)
        return Cluster._interval_distance_with_given_alignment(sample, psv, prototype_band, total_alignment, prototype_in_psv)

    def calculate_distance(self, sample: np.ndarray, mode: str = "interval") -> float:
        """ Calculate the distance of the sample to the prototype, using the ERAL score

        ERAL score with normalization is used to calculate the error in alignment of the sample to the prototype.
        Normalization in ERAL score is done by the length of the overlap of the sample and the prototype.

        ERAL score is further multiplied by (len_sample*len_prototype)/(overlap_len^2) to penalize short overlaps.

        :param sample: Sample to be compared to the prototype
        :return: Distance
        """
        match mode.lower():
            case "eral":
                return self.distance(self.prototype, sample, self.eral_exclusion_zone)
            case "interval":
                return self.interval_distance(self.prototype, sample, self.psv, self.eral_exclusion_zone, self.pdv)
            case _:
                raise ValueError(f"Mode {mode} is not supported. Supported modes are 'eral' and 'interval'.")


    @staticmethod
    def _calculate_crisp_prototype_boundaries(psv: np.ndarray, pcv: np.ndarray, alpha: float) -> tuple[int, int]:
        """ Get the start and end index of the crisp prototype in the PSV

        The crisp prototype is defined in the time points where the PCV is greater than some user-defined
        threshold, for example 0.8 indicating that the prototype is defined at indices where at least 80% of the
        samples were used in conditioning the prototype.

        Choosing :param:`alpha`: 1.0 --> only use region where all samples were used, results in a short prototype, 
        0.0 --> use all samples, results in a long prototype

        :param psv: Prototype Shape Vector
        :param pcv: Prototype Confidence Vector
        :param alpha: Threshold for the PCV: required proportion of samples to be used in conditioning the prototype.
        :return: Tuple of the start and end index of the crisp prototype in the PSV
        """

        assert len(psv) == len(pcv), ("PSV and PCV should have the same length")

        bounding_filter = pcv >= alpha
        start_idx = np.argmax(bounding_filter)
        end_idx = len(bounding_filter) - np.argmax(bounding_filter[::-1])
        return start_idx, end_idx


    def _get_crisp_prototype_boundaries(self) -> tuple[int, int]:
        """ Get the start and end index of the crisp prototype in the PSV

        The crisp prototype is defined in the time points where the PCV is greater than some user-defined
        threshold, for example 0.8 indicating that the prototype is defined at indices where at least 80% of the
        samples were used in conditioning the prototype.

        :return: Tuple of the start and end index of the crisp prototype in the PSV
        """

        start_idx, end_idx = self._calculate_crisp_prototype_boundaries(self.psv, self.pcv, self.alpha)

        return start_idx, end_idx


    def _prototype_defuzzification(self) -> np.ndarray:
        """ Returns the prototype of the cluster

        The prototype is obtained by combining the PSV and the PCV. The prototype is
        only defined in the time points where the PCV is greater than some user-defined threshold, for
        example 0.8 indicating that the prototype is defined at indices where at least 80% of the samples were used
        in conditioning the prototype.

        :return: Crisp prototype
        """

        start_idx, end_idx = self._get_crisp_prototype_boundaries()

        return self.psv[start_idx:end_idx]

    @property
    def prototype(self) -> np.ndarray:
        """ Get the prototype of the cluster """
        return self._prototype_defuzzification()


    def copy(self, deep: bool = False, new_id: int | None = None) -> 'Cluster':
        """ Create a copy of the cluster

        :param deep: If True, a deep copy is made. If False, a shallow copy is made.
        :return: Copy of the cluster
        """

        if new_id is None:
            new_id = self.id

        if not deep:
            new_cluster = self.__class__(sample=self.psv)
            new_cluster.pcv = self.pcv.copy()
            new_cluster.pdv_m2 = self.pdv_m2.copy()
            new_cluster.pdv_m2_count = self.pdv_m2_count.copy()
            new_cluster.initial_std = self.initial_std
            new_cluster.initial_std_count = self.initial_std_count
            new_cluster.number_of_points = self.number_of_points
            new_cluster.alpha = self.alpha
            new_cluster.id = new_id
            new_cluster.eral_exclusion_zone = self.eral_exclusion_zone
            return new_cluster
        
        new_cluster = self.__class__(sample=self.psv.copy(), id = new_id)
        new_cluster.pcv = self.pcv.copy()
        new_cluster.pdv_m2 = self.pdv_m2.copy()
        new_cluster.pdv_m2_count = self.pdv_m2_count.copy()
        new_cluster.initial_std = self.initial_std
        new_cluster.initial_std_count = self.initial_std_count
        new_cluster.number_of_points = self.number_of_points
        new_cluster.alpha = self.alpha
        new_cluster.eral_exclusion_zone = self.eral_exclusion_zone
        return new_cluster
    
    def merge(self, other_cluster: 'Cluster', new_alpha: float | None = None, new_id: int | None = None):
        """ Force merge the other cluster into this cluster
        
        The other cluster is added to this cluster. The prototype is updated by adding the prototype of the other
        cluster to the prototype of this cluster. The PCV is updated to reflect the new number of points.
        
        :param other_cluster: Cluster to be merged into this cluster
        :param new_alpha: New alpha value for the merged cluster. If None, the alpha value of this cluster is used.
        :param new_id: New id for the merged cluster. If None, the id of this cluster is used.
        """

        success = self.try_merge(other_cluster, new_alpha, new_id, min_new_length=0)
        if not success:
            raise Exception("Merge was not successful")
        return

    def try_merge(self, other_cluster: 'Cluster', new_alpha: float | None = None, new_id: int | None = None, min_new_length: float = 0.9) -> bool:
        """ Try to merge the other cluster into this cluster

        The other cluster is added to this cluster. The prototype is updated by adding the prototype of the other
        cluster to the prototype of this cluster. The PCV is updated to reflect the new number of points.

        If the new prototype would be less than `min_new_length` times the length of the old prototype, the merge is not
        performed, False is returned.

        :param other_cluster: Cluster to be merged into this cluster
        :param new_alpha: New alpha value for the merged cluster. If None, the alpha value of this cluster is used.
        :param new_id: New id for the merged cluster. If None, the id of this cluster is used.
        :param min_new_length: Minimum length of the new prototype as a proportion of the old prototype.
        :return: True if the merge was successful, False if the merge was not successful (new prototype would be too short)
        """

        if not isinstance(other_cluster, Cluster):
            raise ValueError(f"Can only merge with another Cluster object, not {type(other_cluster)}")

        my_psv = self.psv
        my_pcv = self.pcv
        my_count = self.number_of_points
        other_psv = other_cluster.psv
        other_pcv = other_cluster.pcv
        other_count = other_cluster.number_of_points

        if new_alpha is None:
            new_alpha = self.alpha
        if new_id is None:
            new_id = self.id

        # my_prototype = self.prototype
        # other_prototype = other_cluster.prototype
        my_prototype_start, my_prototype_end = self._get_crisp_prototype_boundaries()
        my_prototype = my_psv[my_prototype_start:my_prototype_end]
        other_prototype_start, other_prototype_end = other_cluster._get_crisp_prototype_boundaries()
        other_prototype = other_psv[other_prototype_start:other_prototype_end]
        
        # Align the prototypes
        prototype_alignment = get_score_and_shift(my_prototype, other_prototype, exclusion_zone=self.eral_exclusion_zone, apply_zero_mean=False)[1] # TODO: apply zero mean is fixed, check if it should be changed
        alignment = prototype_alignment + my_prototype_start - other_prototype_start
        


        # alignment: int = self._get_alignment_of_sample_to_psv(other_prototype)

        _, shifted_other_pcv, shifted_my_pcv = sync_n_series_to_prototype(prototype=my_pcv,
                                                                                    series=[other_pcv],
                                                                                    shifts=[alignment])
        shifted_other_pcv = shifted_other_pcv[0]
        shifted_other_pcv = np.nan_to_num(shifted_other_pcv, nan=0)
        shifted_my_pcv = np.nan_to_num(shifted_my_pcv, nan=0)
        new_pcv = (my_count * shifted_my_pcv + other_count * shifted_other_pcv) / (my_count + other_count)
        
        # Calculate the new PSV
        _, shifted_other_psv, shifted_my_psv = sync_n_series_to_prototype(prototype=my_psv,
                                                                                    series=[other_psv],
                                                                                    shifts=[alignment])
        shifted_other_psv = shifted_other_psv[0]

        my_points_count = my_count * shifted_my_pcv
        other_points_count = other_count * shifted_other_pcv
        weight_my_psv = my_points_count / (my_points_count + other_points_count)
        weight_other_psv = other_points_count / (my_points_count + other_points_count)

        aligned_my_psv_nan_mask = np.isnan(shifted_my_psv)
        aligned_other_psv_nan_mask = np.isnan(shifted_other_psv)
        
        my_psv_weights_vector = np.zeros_like(shifted_my_psv)+weight_my_psv
        other_psv_weights_vector = np.zeros_like(shifted_other_psv)+weight_other_psv        
        # Weights should be weight_my_psv and weight_other_psv where neither of the values is NaN
        pass

        # At regions where only my_psv is NaN, other_psv should be used
        my_psv_weights_vector[aligned_my_psv_nan_mask] = 0
        other_psv_weights_vector[aligned_my_psv_nan_mask] = 1

        # At regions where only other_psv is NaN, my_psv should be used
        my_psv_weights_vector[aligned_other_psv_nan_mask] = 1
        other_psv_weights_vector[aligned_other_psv_nan_mask] = 0

        # The sum of the weights should be 1
        assert np.allclose(my_psv_weights_vector+other_psv_weights_vector, 1), ("My PSV and other PSV weights should sum to 1")

        weighted_my_psv = shifted_my_psv * my_psv_weights_vector
        weighted_other_psv = shifted_other_psv * other_psv_weights_vector

        new_psv = np.nansum(np.array([weighted_my_psv, weighted_other_psv]), axis=0)


        # Remove padding where pcv is 0
        start_idx = np.argmax(new_pcv>0)
        end_idx = len(new_pcv) - np.argmax(new_pcv[::-1]>0)
        new_psv = new_psv[start_idx:end_idx]
        new_pcv = new_pcv[start_idx:end_idx]
        
        assert len(new_psv) == len(new_pcv), ("New PSV and new PCV should have the same length.")

        final_prototype_start_idx, final_prototype_end_idx = self._calculate_crisp_prototype_boundaries(new_psv, new_pcv, new_alpha)
        final_prototype_length = final_prototype_end_idx - final_prototype_start_idx

        if final_prototype_length < len(my_prototype)*min_new_length:
            return False
        
        _, other_aligned_pdv_m2, my_aligned_pdv_m2 = sync_n_series_to_prototype(prototype=self.pdv_m2,
                                                                                    series=[other_cluster.pdv_m2],
                                                                                    shifts=[alignment])
        other_aligned_pdv_m2 = other_aligned_pdv_m2[0]

        _, other_aligned_pdv_m2_count, my_aligned_pdv_m2_count = sync_n_series_to_prototype(prototype=self.pdv_m2_count,
                                                                                    series=[other_cluster.pdv_m2_count],
                                                                                    shifts=[alignment])
        other_aligned_pdv_m2_count = other_aligned_pdv_m2_count[0]
        
        new_pdv_m2, new_pdv_m2_count = self._get_merged_pdv(my_aligned_pdv_m2, 
                                                            my_aligned_pdv_m2_count, 
                                                            shifted_my_psv,
                                                            other_aligned_pdv_m2, 
                                                            other_aligned_pdv_m2_count,
                                                            shifted_other_psv)
        
        # if start_idx != 0 or end_idx != len(new_pcv):
        new_pdv_m2 = new_pdv_m2[start_idx:end_idx]
        new_pdv_m2_count = new_pdv_m2_count[start_idx:end_idx]
        
        assert len(new_pdv_m2) == len(new_pcv), ("New PDV M2 and new PCV should have the same length. "
                                                                        f"Lengths are {len(new_pdv_m2)} and "
                                                                        f"{len(new_pcv)}")
        assert len(new_pdv_m2_count) == len(new_pcv), ("New PDV M2 count and new PCV should have the same length. "
                                                                        f"Lengths are {len(new_pdv_m2_count)} and "
                                                                        f"{len(new_pcv)}")
        
        assert np.count_nonzero(np.isnan(new_pdv_m2_count)) == 0, ("New PDV M2 count should not have NaN values")
        assert np.count_nonzero(np.isnan(new_pdv_m2)) == 0, ("New PDV M2 should not have NaN values")

        # Update the cluster
        self.psv = new_psv
        self.pcv = new_pcv
        self.pdv_m2 = new_pdv_m2
        self.pdv_m2_count = new_pdv_m2_count
        self.number_of_points += other_count
        self.alpha = new_alpha
        self.id = new_id

        return True

    @staticmethod    
    def _get_merged_pdv(my_aligned_pdv_m2: np.ndarray, 
                        my_aligned_pdv_m2_count: np.ndarray,
                        my_aligned_psv: np.ndarray,
                        other_aligned_pdv_m2: np.ndarray, 
                        other_aligned_pdv_m2_count: np.ndarray,
                        other_aligned_psv: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """ Get the merged PDV M2 and PDV M2 count vectors """
        assert len(my_aligned_pdv_m2) == len(my_aligned_pdv_m2_count), ("My PDV M2 and PDV M2 count should have the same length")
        assert len(my_aligned_pdv_m2) == len(my_aligned_psv), ("My PDV M2 and my PSV should have the same length")
        assert len(other_aligned_pdv_m2) == len(other_aligned_pdv_m2_count), ("Other PDV M2 and PDV M2 count should have the same length")
        assert len(other_aligned_pdv_m2) == len(other_aligned_psv), ("Other PDV M2 and other PSV should have the same length")
        assert len(my_aligned_pdv_m2) == len(other_aligned_pdv_m2), ("My PDV M2 and other PDV M2 should have the same length")
        
        my_aligned_pdv_m2 = np.nan_to_num(my_aligned_pdv_m2, nan=0)
        my_aligned_pdv_m2_count = np.nan_to_num(my_aligned_pdv_m2_count, nan=0)
        other_aligned_pdv_m2 = np.nan_to_num(other_aligned_pdv_m2, nan=0)
        other_aligned_pdv_m2_count = np.nan_to_num(other_aligned_pdv_m2_count, nan=0)

        psv_delta = other_aligned_psv - my_aligned_psv
        psv_delta[np.isnan(psv_delta)] = 0

        new_pdv_m2_count = my_aligned_pdv_m2_count + other_aligned_pdv_m2_count
        new_pdv_m2 = my_aligned_pdv_m2 + other_aligned_pdv_m2 + psv_delta**2 * my_aligned_pdv_m2_count * other_aligned_pdv_m2_count / new_pdv_m2_count
        
        return new_pdv_m2, new_pdv_m2_count
