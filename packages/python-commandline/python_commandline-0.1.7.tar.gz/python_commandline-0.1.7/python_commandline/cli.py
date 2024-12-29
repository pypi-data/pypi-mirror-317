import os
import platform
import shutil
import site
import zipfile
from pathlib import Path

import dotenv
import fire
import tomllib
from pydantic import BaseModel


class Command:
    def zip_file(self, src: str, dst: str) -> None:
        """
        Zip a file to a specified zip file

        Args:
            src (str): Path to the source file.
            dst (str): Path to the destination ZIP file.
        """
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
            full_path = os.path.abspath(src)
            archive_path = os.path.relpath(full_path, os.path.dirname(src))
            zip_file.write(full_path, archive_path)

    def zip_dir(self, src: str, dst: str) -> None:
        """
        Zips the contents of a directory to a specified zip file

        Args:
            src (str): Path to the source directory.
            dst (str): Path to the destination ZIP file.
        """
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
            for root, _, files in os.walk(src):
                for file in files:
                    full_path = os.path.join(root, file)
                    archive_path = os.path.relpath(full_path, os.path.dirname(src))
                    zip_file.write(full_path, archive_path)

    def get_cpu_arch(self) -> str:
        arch = platform.machine()
        if arch == "AMD64":
            return "x86_64"
        return arch

    def get_os(self) -> str:
        system_name = platform.system()
        system_map = {
            "Windows": "Windows",
            "Linux": "Linux",
            "Darwin": "macOS"
        }
        return system_map.get(system_name, "Unknown system")

    def get_site_packages_dir(self) -> str:
        dirs = site.getsitepackages()
        for d in dirs:
            if "site-packages" in d:
                return d
        raise RuntimeError(f"Faild to find site-packages dir in {dirs}")

    def get_version(self) -> str:
        return self.get_version_from_pyproject()

    def get_version_from_config(self, module_name: str, class_name: str, field_name: str) -> str:
        cls = self.read_class_from_module(module_name, class_name)
        obj = cls()
        return getattr(obj, field_name)

    def get_version_from_pyproject(self) -> str:
        try:
            # Load the pyproject.toml file
            with Path("pyproject.toml").open("rb") as toml_file:
                toml_data = tomllib.load(toml_file)

            # Get the version from [tool.poetry] section
            version: str = toml_data.get("tool", {}).get("poetry", {}).get("version")
            if version:
                return version

            raise ValueError("Version not found in pyproject.toml [tool.poetry] section.")
        except FileNotFoundError as e:
            raise FileNotFoundError("File pyproject.toml not found.") from e
        except Exception as e:
            raise Exception(f"Error while parsing pyproject.toml: {str(e)}") from e


    def set_env(self) -> None:
        dotenv.set_key(".env", "version", self.get_version())

    def copy_dir(self, src: str, dst: str) -> None:
        shutil.copytree(src, dst, dirs_exist_ok=True)

    def copy_file(self, src: str, dst: str) -> None:
        shutil.copy(src, dst)

    def mkdirs(self, path: str) -> None:
        Path(path).mkdir(parents=True, exist_ok=True)

    def move(self, src: str, dst: str) -> None:
        shutil.move(src, dst)

    def read_class_from_module(self, module_name: str, class_name: str):
        """
        Reads a specified field from a specified Pydantic model class in a specified module.

        Args:
            module_name (str): The name of the module file (without .py) to import.
            class_name (str): The name of the Pydantic model class to access.

        Returns:
            The specified class.

        Raises:
            ImportError: If the module cannot be imported.
            AttributeError: If the class does not exist.
            TypeError: If the class is not a subclass of BaseModel.
        """
        import importlib.util
        import os

        try:
            # Construct the module file path
            module_file_path = os.path.join(os.getcwd(), f"{module_name}.py")
            spec = importlib.util.spec_from_file_location(module_name, module_file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Get the specified class
            cls = getattr(module, class_name)

            # Check if the class is a subclass of BaseModel
            if not issubclass(cls, BaseModel):
                raise TypeError(f"Class '{class_name}' is not a subclass of BaseModel.")

            return cls
        except FileNotFoundError as e:
            raise ImportError(f"Module file '{module_name}.py' not found: {str(e)}") from e
        except AttributeError as e:
            raise AttributeError(f"Class '{class_name}' not found: {str(e)}") from e

def main() -> None:
    fire.Fire(Command)


if __name__ == "__main__":
    main()
