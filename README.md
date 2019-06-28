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
>>> from hyperspy_swift_libray import SwiftLibraryReader
>>> lib = SwiftLibraryReader("Nion Swift Library 20190531/")
>>> lib.list_data_items(signal_type="image")
1
	Title: Snapshot of SuperScan (DF)
	Created: 2019-05-31T07:48:37.744457
	Shape: [512, 512]
	Datum dimension: 2
2
	Title: SuperScan (DF)
	Created: 2019-05-31T07:48:37.744457
	Shape: [512, 512]
	Datum dimension: 2
>>> lib.load_data(2, lazy=True)
<LazySignal2D, title: , dimensions: (|512, 512)>
```
