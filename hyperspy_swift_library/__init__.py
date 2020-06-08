import pathlib

from nion.swift.model import DocumentModel
from nion.swift.model import DataItem
from nion.swift.model import FileStorageSystem
from nion.swift.model import Profile
import dask.array as da
from hyperspy.misc.utils import DictionaryTreeBrowser
from hyperspy._signals.signal1d import Signal1D, LazySignal1D
from hyperspy._signals.signal2d import Signal2D, LazySignal2D

__version__ = "0.1"


def get_storage_system(workspace_dir):
    # This function is adapted from Swift's profile
    workspace_dir = pathlib.Path(workspace_dir)
    library_path = Profile._migrate_library(workspace_dir, do_logging=True)
    this_storage_version = DataItem.DataItem.storage_version
    auto_migrations = list()
    auto_migrations.append(
        Profile.AutoMigration(
            pathlib.Path(workspace_dir) /
            "Nion Swift Workspace.nslib",
            [
                pathlib.Path(workspace_dir) /
                "Nion Swift Data"]))
    auto_migrations.append(
        Profile.AutoMigration(
            pathlib.Path(workspace_dir) /
            "Nion Swift Workspace.nslib",
            [
                pathlib.Path(workspace_dir) /
                "Nion Swift Data 10"]))
    auto_migrations.append(
        Profile.AutoMigration(
            pathlib.Path(workspace_dir) /
            "Nion Swift Workspace.nslib",
            [
                pathlib.Path(workspace_dir) /
                "Nion Swift Data 11"]))
    # Attemp at being future proof
    if this_storage_version > 12:
        for storage_version in range(12, this_storage_version):
            auto_migrations.append(
                Profile.AutoMigration(pathlib.Path(workspace_dir) / f"Nion Swift Library {storage_version}.nslib",
                                      [pathlib.Path(workspace_dir) / f"Nion Swift Data {storage_version}"]))

    # NOTE: when adding an AutoMigration here, also add the corresponding file
    # copy in _migrate_library
    storage_system = FileStorageSystem.FileStorageSystem(library_path, [pathlib.Path(
        workspace_dir) / f"Nion Swift Data {this_storage_version}"], auto_migrations=auto_migrations)
    return storage_system


def axes_swift2hspy(axes, shape):
    for axis, dim in zip(axes, shape):
        axis["size"] = dim
    return axes


class SwiftLibraryReader:
    def __init__(self, workspace_dir):
        self._storage_system = get_storage_system(workspace_dir)
        self._data_items = sorted(
            self._storage_system.find_data_items(),
            key=lambda x: x.read_properties()["created"])
        self._data_items_properties = [
            di.read_properties() for di in self._data_items]

    def list_data_items(self, signal_type=None, list_print=True):
        dict_data = {}
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
            if list_print == True:
                print(f"{i}")
                print(f'\tTitle: {md["title"]}')
                print(f'\tCreated: {md["created"]}')
                print(f'\tShape: {md["data_shape"]}')
                print(f'\tDatum dimension: {md["datum_dimension_count"]}')
            if "title" in dict_data:
                dict_data["title"].append(md["title"])
            else:
                dict_data["title"] = [md["title"]]
            if "data_shape" in dict_data:
                dict_data["data_shape"].append(md["data_shape"])
            else:
                dict_data["data_shape"] = [md["data_shape"]]
            if "datum_dimension_count" in dict_data:
                dict_data["datum_dimension_count"].append(md["datum_dimension_count"])
            else:
                dict_data["datum_dimension_count"] = [md["datum_dimension_count"]]
            if "created" in dict_data:
                dict_data["created"].append(md["created"])
            else:
                dict_data["created"] = [md["created"]]
        return dict_data

    def load_data(self, num, lazy=True):
        handler = self._data_items[num]
        md = self._data_items_properties[num]
        if md["datum_dimension_count"] == 1:
            Signal = LazySignal1D if lazy else Signal1D
        elif md["datum_dimension_count"] == 2:
            Signal = LazySignal2D if lazy else Signal2D
        data = handler.read_data()
        if lazy:
            data = da.from_array(data)
        signal = Signal(
            data=data,
            axes=axes_swift2hspy(
                md["dimensional_calibrations"],
                shape=md["data_shape"]))
        signal.original_metadata.add_dictionary(md)
        return signal


