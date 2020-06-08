# Hyperspy Swift Library

Read Nion Swift libraries into HyperSpy object.


## Installation

This package depends on [Nion Swift](https://github.com/nion-software/nionswift). [Installing
it](https://nionswift.readthedocs.io/en/stable/installation.html) with ``conda``
before installing ``hyperspy_swift_library`` is recommended.


```bash
pip install --upgrade https://github.com/hyperspy/hyperspy_swift_library/archive/master.tar.gz
```

## Usage

```python
>>> from hyperspy_swift_library import SwiftLibraryReader
>>> import pandas as pd
>>> lib = SwiftLibraryReader("Nion Swift Library 20200606/")
>>> lib.list_data_items(signal_type="image")
0
	Title: HADF
	Created: 2020-06-06T11:04:36.368747
	Shape: [2048, 2048]
	Datum dimension: 2
1
	Title: LowMag2_TEM
	Created: 2020-06-06T11:05:57.354602
	Shape: [520, 696]
	Datum dimension: 2
2
	Title: LowMag1_TEM
	Created: 2020-06-06T11:05:57.405164
	Shape: [520, 696]
	Datum dimension: 2

>>> lib.load_data(2, lazy=True)
<LazySignal2D, title: , dimensions: (|512, 512)>

>>> df = lib.get_data_items()
>>> df["title"]
0           HADF
1    LowMag2_TEM
2    LowMag1_TEM
Name: title, dtype: object

>>> df[df["title"].str.endswith("_TEM")] # Can be used for filtering based on "title"
```
