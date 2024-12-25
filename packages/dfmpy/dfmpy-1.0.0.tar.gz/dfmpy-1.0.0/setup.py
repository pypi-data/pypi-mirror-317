# /usr/bin/env python3

import functools
import io
import pathlib
import shutil

# pylint: disable=import-error

import setuptools
import setuptools.command.install

PROJECT_NAME = "dfmpy"
PROJECT_VERSION = "1.0.0"


@functools.lru_cache(maxsize=2)
def get_repo_file_name(filename) -> pathlib.Path:
    """
    Returns the filename that is relative to the project directory as a file
    path.

    :param pathlib.Path|str filename: The relative file path.

    :rtype: pathlib.Path
    :return: The path to the specified file.
    """
    project_directory = pathlib.Path(__file__).resolve().parent
    filename = project_directory.joinpath(filename)
    return filename


@functools.lru_cache(maxsize=2)
def read_repo_file(filename):
    """
    Reads the specified file and returns the full contents as a single string.

    :param pathlib.Path|str filename: The file to read.

    :rtype: str
    :return: The full contents of the specified file.
    """
    file_path = get_repo_file_name(filename)
    return file_path.read_text(encoding="UTF-8")


def load_requirements(filename):
    """
    Loads the :code:`requirements.tx` dependency file and returns the
    dependencies as a sequence.

    The file can contain comments that follow the pound symbol (eg. '#').
    Comments will be removed, each line is stripped of leading and trailing
    whitespace, and empty lines are deleted.  Other than these basic
    transformations, the requirements are left intact.

    :param pathlib.Path|str filename: The requirements file to read.

    :rtype: tuple
    :return: A sequence of requirements.
    """
    reqs = read_repo_file(filename).splitlines()
    reqs = [str(x).strip() for x in reqs]
    reqs = [x[: x.find("#")] for x in reqs if "#" in x]
    reqs = [x for x in reqs if len(x)]
    return tuple(reqs)


def get_dfmpy_packages():
    """
    Finds all packages within this project and only returns the production ready
    ones.  Meaning, test packages will not be included.

    :rtype tuple
    :return: A sequence of package names that will be built into the file
            distribution.
    """
    packages = setuptools.find_packages()
    packages = [p for p in packages if not p.endswith("_test")]
    return tuple(packages)


class CleanCommand(setuptools.Command):
    """
    A custom clean command that removes any intermediate build directories.
    """

    description = (
        "Custom clean command that forcefully removes build, dist,"
        " and other similar directories."
    )
    user_options = []

    def __init__(self, *args, **kwargs):
        """Initialized the custom clean command with a list of directories."""
        super().__init__(*args, **kwargs)
        project_path = pathlib.Path(__file__).resolve().parent
        self._clean_paths = {
            ".eggs",
            "build",
            PROJECT_NAME + ".egg-info",
            "dist",
            ".coverage",
            "coverage.xml",
            ".pytest_cache",
        }
        self._clean_paths = {project_path.joinpath(p) for p in self._clean_paths}
        self._clean_paths = {d for d in self._clean_paths if d.exists()}

    def initialize_options(self):
        """Unused, but required when implementing :class:`setuptools.Command`."""
        # pylint: disable=unnecessary-pass
        pass

    def finalize_options(self):
        """Unused, but required when implementing :class:`setuptools.Command`."""
        # pylint: disable=unnecessary-pass
        pass

    def run(self):
        """Performs the actual removal of the intermediate build directories."""
        for path in self._clean_paths:
            if path.is_dir():
                print(f"Removing directory {path}")
                shutil.rmtree(path)
            elif path.is_file():
                print(f"Removing file {path}")
                path.unlink()
            else:
                print(f"ERROR: Unknown file type: {path}")


# pylint: disable=too-few-public-methods
class InstallCommand(setuptools.command.install.install):
    """
    Custom command to install dependencies cause setuptools sucks balls and does
    not honor the "install_requires" parameter.  Apparently the default
    functionality is to run in backward-compatibile mode, which does not install
    the project's dependencies  :-(

    @see https://github.com/pypa/setuptools/issues/456#issuecomment-202922033
    """

    def run(self):
        """
        Performs the installation of dependencies, based on the
        :code:`requirements.txt` and :code:`requirements-test.txt` files.
        """
        # Need to run the original "install" first.
        super().run()

        # Not sure why, but moving these up to the top-level, and use the
        # "from PACKAGE import NAME" format, did not work.
        # pylint: disable=import-outside-toplevel
        import subprocess

        # pylint: disable=import-outside-toplevel
        import sys

        files = ("requirements.txt", "requirements-test.txt")
        files = [get_repo_file_name(f) for f in files]
        for req_file in files:
            print(f"Installing dependencies from: {req_file}")
            command_line = ("python3", "-m", "pip", "install", "-r", req_file)
            with subprocess.Popen(command_line, stdout=subprocess.PIPE) as proc:
                for line in io.TextIOWrapper(proc.stdout, encoding="UTF-8"):
                    sys.stdout.write(line)


setuptools.setup(
    name=PROJECT_NAME,
    version=PROJECT_VERSION,
    author="Mike Durso",
    author_email="rbprogrammer@gmail.com",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    cmdclass={
        "clean": CleanCommand,
        "install": InstallCommand,
    },
    description="Another dotfiles manager.",
    entry_points={
        "console_scripts": [
            "dfm = dfmpy.__main__:main",
        ]
    },
    install_requires=load_requirements("requirements.txt"),
    long_description=read_repo_file("README.md"),
    long_description_content_type="text/markdown",
    packages=get_dfmpy_packages(),
    package_data={"dfmpy.resources": ["*"]},
    test_suite="dfmpy_test",
    tests_require=load_requirements("requirements-test.txt"),
    url="https://gitlab.com/deliberist/dfmpy",
)
