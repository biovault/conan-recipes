from conans import ConanFile
from conans.tools import load, save
from pathlib import Path
from shutil import copytree
import tempfile
import os
import inspect 

class BundleUtils(object):
    # Default is to merge Debug & RelWithDebInfo to Release
    # Override this in the child class if needed
    _merge_from = ["Debug", "RelWithDebInfo"]
    _merge_to = "Release"  

    def _get_temp_save_dir(self):
        return Path(tempfile.gettempdir(), self.name)
    
    def _save_git_path(self):
        # Must be called from conan init or export as the
        # working directory is the git path at that point
        if inspect.stack()[1].function != "init" and inspect.stack()[1].function != "export":
            raise RuntimeError("_save_git_path must be called from conan init or export")
        caller_dir = Path(os.getcwd()).resolve()
        save(
            Path(self._get_temp_save_dir(), "__gitpath.txt"),
            str(caller_dir)
        )

    def __get_git_path(self):
        path = load(
            Path(self._get_temp_save_dir(), "__gitpath.txt")
        )
        return path

    def _save_package_id(self, build_type=None):
        if build_type is None:
            build_type = self.settings.build_type
        package_id = self.info.package_id()
        idfile = Path(self.__get_git_path(), f"{build_type}_id.txt")
        with open(idfile, "w") as pidfile:
            pidfile.write(f"{package_id}")

    def _get_package_id(self, build_type):
        idfile = Path(self.__get_git_path(), f"{build_type}_id.txt")
        package_id = None
        if idfile.exists():
            with open(idfile, "r") as pidfile:
                package_id = pidfile.read().rstrip()
        return package_id
    
    def _merge_packages(self):
        if self.options.merge_package:
            # Merge any other available packages into the merge target package
            target_id = self._get_package_id(self._merge_to)
            merge_target_dir = Path(self.package_folder, "..", target_id).resolve()
            for build_type in self._merge_from:
                source_id = self._get_package_id(build_type)
                if source_id is not None:
                    print(f"Merging package {build_type} into {self._merge_to}")
                    merge_source_dir = Path(self.package_folder, "..", source_id).resolve()
                    if merge_source_dir.exists():
                        copytree(merge_source_dir, merge_target_dir, dirs_exist_ok=True)


class BundlePackage(ConanFile):
    name = "bundleutils"
    version = "0.1"