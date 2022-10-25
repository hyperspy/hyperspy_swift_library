from nion.swift.model import Persistence
from nion.swift.model import Profile
from nion.swift.model import Project
from nion.swift.model import HardwareSource
import pathlib
import typing
import dask.array as da
from hyperspy.misc.utils import DictionaryTreeBrowser
from hyperspy._signals.signal1d import Signal1D, LazySignal1D
from hyperspy._signals.signal2d import Signal2D, LazySignal2D
import os

__version__ = "0.2"




def axes_swift2hspy(axes, shape):
    for axis, dim in zip(axes, shape):
        axis["size"] = dim
    return axes


class SwiftLibraryReader:
    """Load items in Nion Swift project with HyperSpy"""

    def __init__(self, project_file_path):
        """Parse Nion Swift project file
        
        Parameters
        ----------
        project_file_path: str
            The path of the Nion Swift project file with extension `.nsproj`.
        """
        current_path = os.getcwd()
        file_path = pathlib.Path(project_file_path)

        if not os.path.isfile(file_path):
            raise ValueError(f"The file {project_file_path} does not exist")
        if file_path.suffix == ".nsproj":
            r = Profile.IndexProjectReference()
            r.project_path = file_path
        else:
            raise ValueError("Please provide a file with extension `.nsproj`")
        r.persistent_object_context = Persistence.PersistentObjectContext()
        r.load_project(None, pathlib.Path("."), cache_factory=None)
        #  r.project._raw_properties["version"] = 3
        r.project.read_project()
        self._idp = r

    def print_data_item_titles_sizes(self) -> None:
        """Print data items and the shape of the data array.
        """
        p = self._idp.project
        for data_item in p.data_items:
            if data_item.xdata:
                print(f"{data_item.title}: {data_item.xdata.data.shape}")
            else:
                print(f"{data_item.title}: This item does not contain data")

    def get_data_items_properties(self):
        """Data items properties

        Returns
        ----------

        properties : pandas.DataFrame or dictionary
            Pandas DataFrame containing data_items properties if Pandas is installed; otherwise a dictionary containing the same data.

        """

        p = self._idp.project
        properties = {}
        for data_item in p.data_items:
            if data_item.xdata:
                for key in data_item.properties.keys():
                    if key in properties.keys():
                        properties[key].append(data_item.properties[key])
                    else:
                        properties[key] = [data_item.properties[key]]
            else:
                for item in properties.items():
                    if item[0] == "title":
                        item[1].append(data_item.properties["title"])
                    else:
                        item[1].append("<Not data>")

        try:
            import pandas as pd
            df = pd.DataFrame(properties)
            return df
        except ImportError as e:
            return properties

    def load_data(self, num, lazy=True):
        """The data item in a HyperSpy signal
        
        Parameters:
        ----------
        num: int
            The index of the data item.
        lazy: bool
            If True, the data is not loaded into memory.
        """
        project = self.read_project()
        handler = project.data_items[num]
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