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
        self = r.project



    def list_data_items(self):
        print(dir(self))
        return 0


    def load_data(self):
        handler = self._data_items[num]
        return 0