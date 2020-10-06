from nion.swift.model import Persistence
from nion.swift.model import Profile
from nion.swift.model import Project
import pathlib
import typing
import dask.array as da
from hyperspy.misc.utils import DictionaryTreeBrowser
from hyperspy._signals.signal1d import Signal1D, LazySignal1D
from hyperspy._signals.signal2d import Signal2D, LazySignal2D
from importlib.metadata import version

__version__ = "0.1"


def axes_swift2hspy(axes, shape):
    for axis, dim in zip(axes, shape):
        axis["size"] = dim
    return axes

class SwiftLibraryReader:
    def __init__(self, file_path):
        file_path = pathlib.Path(file_path)
        if file_path.suffix == ".nsproj":
            r = Profile.IndexProjectReference()
            r.project_path = file_path
        else:
            r = Profile.FolderProjectReference()
            r.project_folder_path = file_path
        r.persistent_object_context = Persistence.PersistentObjectContext()
        r.load_project(None)
        #r.project._raw_properties["version"] = 3
        r.project.read_project()
        r.project.read_project()
        self.project = r.project
        self._data_items_properties = [
            di.properties for di in self.project.data_items]

    def list_data_items(self, signal_type=None):
        for i, md in enumerate(self._data_items_properties):
            if signal_type == "ndspectrum":
                if md["datum_dimension_count"] != 1 or md["data_shape"][0] < 2:
                    continue
            elif signal_type == "spectrum":
                if md["datum_dimension_count"] != 1 or md["data_shape"][0] > 1:
                    continue
            elif signal_type == "image":
                if md["datum_dimension_count"] != 2 or len(
                        md["data_shape"]) != 2:
                    continue
            elif signal_type == "ndimage":
                if md["datum_dimension_count"] != 2 or len(
                        md["data_shape"]) < 3:
                    continue
            elif signal_type is not None:
                raise ValueError(
                    "signal_type must be one of: ndspectrum, spectrum, ndimage, image, not %s" %
                    signal_type)
            datum_dimension_count = 1
            print(f"{i}")
            print(f'\tTitle: {md["title"]}')
            print(f'\tCreated: {md["created"]}')
            print(f'\tShape: {md["data_shape"]}')
            print(f'\tDatum dimension: {md["datum_dimension_count"]}')

    def get_data_items(self):
        """Creates a DataFrame containing data_items properties in a NionSwift library

        Returns
        ----------

        DataFrame : Pandas DataFrame containing data_items properties if Pandas is installed; otherwise a dictionary containing the same data.

        Examples
        --------

        >>> df["title"]
        0           HADF
        1    LowMag2_TEM
        2    LowMag1_TEM
        Name: title, dtype: object

        >>> df[df["title"].str.endswith("_TEM")] # can be used for filtering based on "title".

        """
        try:
            import pandas as pd
            df = pd.DataFrame(self._data_items_properties)
            return df
        except ImportError as e:
            properties = self._data_items_properties
            return properties


    def load_data(self, num, lazy=True):
        handler = self.project.data_items[num]
        md = handler.properties
        if md["datum_dimension_count"] == 1:
            Signal = LazySignal1D if lazy else Signal1D
        elif md["datum_dimension_count"] == 2:
            Signal = LazySignal2D if lazy else Signal2D
        data = handler.data
        if lazy:
            data = da.from_array(data)
        signal = Signal(
            data=data,
            axes=axes_swift2hspy(
                md["dimensional_calibrations"],
                shape=md["data_shape"]))
        signal.original_metadata.add_dictionary(md)
        return signal
