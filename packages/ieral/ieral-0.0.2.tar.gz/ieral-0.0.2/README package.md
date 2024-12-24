# Interval ERAL Algorithm and application to Evolving Clustering

## Introduction
The iERAL (Interval Error In Alignment) algorithm is a state-of-the-art method designed for online time series alignment and averaging.
The method obtains the average time series (the prototype) from a set of time series (a class).

## Installation

To use iERAL, please install the package from pypi.org using pip:
```bash
pip install ieral
```

## Usage

The main entry point for the end user is `Cluster` class in `ieral.ieral`:

```py
from ieral.ieral import Cluster as iERAL

ieral = iERAL(sample=initial_sample, id=0)
```

The class constructor accepts two parameters:
- `sample` - the initial sample to be used for the prototype calculation
- `id` - the class identifier

The basic function call is:

```py
import numpy as np
from ieral.ieral import Cluster as iERAL

data: list[np.ndarray] = [...]

ieral: iERAL = iERAL(sample=data[0], id=id, alpha=0.5)
for sample in data[1:]:
    ieral.add_sample(sample=sample)

prototype = ieral.prototype
    
```

For full examples, please refer to the `examples/` directory at [our repository](https://repo.ijs.si/zstrzinar/ieral).

## Demonstration
The following figure demonstrates iERAL algorithm on a set of time series from the Trace dataset from UCR Archive. The dataset contains 100 time series, each with 275 samples. The time series are aligned and averaged using iERAL, and the resulting prototype is shown in the figure.
![iERAL demonstration](https://repo.ijs.si/zstrzinar/ieral/-/raw/0cc738be42d7e26bfbca8914dd5aa4ef1dbb6e21/docs/assets/trace.png)

## Examples

The `examples/` directory at [our repository](https://repo.ijs.si/zstrzinar/ieral). contains Jupyter notebooks that illustrate different uses and capabilities of the iERAL algorithm. 
To run an example, navigate to the `examples/` directory and execute the desired notebook.

- Notebook titled `01 iERAL demo` demonstrates the iERAL prototyping method using the Trace dataset from UCR Archive.
- Notebook titled `02 iERAL demo on industrial data` downloads an industrial dataset from Mendeley Data [2], and calculates the prototypes for all classes.
- Notebook titled `03 iERAL vs ERAL vs DBA vs SBD` demonstrates the performance of iERAL, ERAL, DBA, and SBD algorithms on the industrial dataset from [2].
- Notebook titled `04 Evolving Time Series Clustering` demonstrates the application of iERAL in the Evolving Time Series Clustering method [1].

## References
[1]  \
[2] Stržinar, Žiga; Pregelj, Boštjan; Petrovčič, Janko; Škrjanc, Igor; Dolanc, Gregor (2024), “Pneumatic Pressure and Electrical Current Time Series in Manufacturing”, Mendeley Data, V2, doi: 10.17632/ypzswhhzh9.2, url: https://data.mendeley.com/datasets/ypzswhhzh9/2
