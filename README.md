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
>>> project = SwiftLibraryReader("Nion Swift Project 20221025.nsproj")
```

If [pandas]() is installed, the `get_data_items_properties` returns a Pandas `DataFrame`.

Using Pandas syntax, it is very easy to select the information that you want to display.
For example, to display only the title and data_shape columns of the `DataFrame`:

```python
>>> df = project.get_data_items_properties()
>>> df[["title", "data_shape"]]
                                title        data_shape
0                                EELS       [128, 1024]
1                     Orsay Scan (BF)        [512, 512]
2                                EELS            [1024]
3              Orsay Scan (eels_spim)  [256, 256, 1024]
4  Pick Sum of Orsay Scan (eels_spim)        <Not data>
```

To filter data based on its title:

```python
>>> df[df['title'].str.endswith("(BF)")]['title']
1    Orsay Scan (BF)
Name: title, dtype: object
```

To load data as a HyperSpy signal:

```python
>>> s = project.load_data(0)
>>> s
<LazySignal2D, title: , dimensions: (|1024, 128)>
```
