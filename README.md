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
>>> project = SwiftLibraryReader("Nion Swift Library 20200606/")
>>> project.print_data_item_titles_sizes()

h-BN_Spectrum_Orsay: (1033,)
h-BN_Spectrum_Orsay_2D: (2000, 1033)

>>> df = project.get_data_items()
>>> df["title"]
0       h-BN_Spectrum_Orsay
1    h-BN_Spectrum_Orsay_2D
Name: title, dtype: object

>>> df[df['title'].str.endswith("_2D")]['title'] Can be used for filtering based on "title"

1    h-BN_Spectrum_Orsay_2D
Name: title, dtype: object

```
