from nion.swift.model import Persistence
from nion.swift.model import Profile
from nion.swift.model import Project
import pathlib
import typing
import dask.array as da
from hyperspy.misc.utils import DictionaryTreeBrowser
from hyperspy._signals.signal1d import Signal1D, LazySignal1D
from hyperspy._signals.signal2d import Signal2D, LazySignal2D

__version__ = "0.1"




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
        r.project._raw_properties["version"] = 3
        r.project.read_project()
        r.project.read_project()
        self.project = r.project



    def list_data_items(self):
        for data_item in self.project.data_items:
            print(data_item.title)



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
            data=data)
        signal.original_metadata.add_dictionary(md)
        #Needs to reshape axes to match those of hyperspy. Needs to test for a spim. Needs to add metadata correctly
        return signal
