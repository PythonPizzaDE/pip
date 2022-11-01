import os
import pathlib

from optparse import Values
from typing import List

from pip._internal.cli.base_command import Command
from pip._internal.cli.status_codes import ERROR, SUCCESS
from pip._internal.utils.logging import getLogger
from pip._internal.utils.misc import get_pip_version

logger = getLogger(__name__)



class InitCommand(Command):
    """
    Init an empty Python project.
    """

    usage = """
    %prog [options]
    """
    gitignore = """# general things to ignore
build/
dist/
*.egg-info/
*.egg
*.py[cod]
__pycache__/
*.so
*~

# due to using tox and pytest
.tox
.cache """

    pyproject_toml = """[build-system]
# These are the assumed default build requirements from pip:
# https://pip.pypa.io/en/stable/reference/pip/#pep-517-and-518-support
requires = ["setuptools>=43.0.0", "wheel"]
build-backend = "setuptools.build_meta" """

    setup_cfg = """[metadata]
# This includes the license file(s) in the wheel.
# https://wheel.readthedocs.io/en/stable/user_guide.html#including-license-files-in-the-generated-wheel-file
license_files = LICENSE.txt"""

    tox_ini = """# this file is *not* meant to cover or endorse the use of tox or pytest or
# testing in general,
#
#  It's meant to show the use of:
#
#  - check-manifest
#     confirm items checked into vcs are in your sdist
#  - python setup.py check
#     confirm required package meta-data in setup.py
#  - readme_renderer (when using a ReStructuredText README)
#     confirms your long_description will render correctly on PyPI.
#
#  and also to help confirm pull requests to this project.

[tox]
envlist = py{37,38,39,310}

# Define the minimal tox version required to run;
# if the host tox is less than this the tool with create an environment and
# provision it with a tox that satisfies it under provision_tox_env.
# At least this version is needed for PEP 517/518 support.
minversion = 3.3.0

# Activate isolated build environment. tox will use a virtual environment
# to build a source distribution from the source tree. For build tools and
# arguments use the pyproject.toml file as specified in PEP-517 and PEP-518.
isolated_build = true

[testenv]
deps =
    check-manifest >= 0.42
    # If your project uses README.rst, uncomment the following:
    # readme_renderer
    flake8
    pytest
commands =
    check-manifest --ignore 'tox.ini,tests/**'
    # This repository uses a Markdown long_description, so the -r flag to
    # `setup.py check` is not needed. If your project contains a README.rst,
    # use `python setup.py check -m -r -s` instead.
    python setup.py check -m -s
    flake8 .
    py.test tests {posargs}

[flake8]
exclude = .tox,*.egg,build,data
select = E,W,F"""

    @staticmethod
    def generate_setup_py(project_name: str) -> None:
        return f"""\"\"\"A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
\"\"\"

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="{project_name}",
    version="2.0.0",
    classifiers=[],
    python_requires=">=3.7, <4",
    extras_require={{
        "dev": ["check-manifest"],
        "test": ["coverage"],
    }},
    project_urls={{
        "Bug Reports": "https://github.com/your/project/issues",
        "Say Thanks!": "http://saythanks.io/to/example",
        "Source": "https://github.com/your/project/",
    }},
)
"""

    @staticmethod
    def generate_readme(project_name: str) -> None:
        return f"# {project_name}\n"

    def add_options(self) -> None:
        self.cmd_opts.add_option("-f", "--folder", dest="target_dir", default=".",
                                 help="folder to initialize project in")

    def run(self, options: Values, args: List[str]) -> int:
        logger.verbose("Using %s", get_pip_version())
        project_path = pathlib.Path(options.target_dir)

        project_name = input("Project name: ")

        if not os.path.exists(project_path.absolute()):
            os.mkdir(project_path.absolute())

        # creating project directories
        os.mkdir((project_path / "src").absolute())
        os.mkdir((project_path / "tests").absolute())
        os.mkdir((project_path / f"src/{project_name}").absolute())

        # TODO: find cleaner way
        # create empty __init__.py files in src/<project_name> and tests directory
        open((project_path / f"src/{project_name}/__init__.py").absolute(), "w").close()
        open((project_path / "tests/__init__.py").absolute(), "w").close()

        # create empty LICENSE.txt
        open((project_path / "LICENSE.txt").absolute(), "w").close()

        with open((project_path / ".gitignore").absolute(), "w") as gitignore_file:
            gitignore_file.write(self.gitignore)

        with open((project_path / "README.md").absolute(), "w") as readme_file:
            readme_file.write(self.generate_readme(project_name))

        with open((project_path / "pyproject.toml").absolute(), "w") as pyproject_file:
            pyproject_file.write(self.pyproject_toml)

        with open((project_path / "setup.cfg").absolute(), "w") as setup_cfg_file:
            setup_cfg_file.write(self.setup_cfg)

        with open((project_path / "setup.py").absolute(), "w") as setup_py_file:
            setup_py_file.write(self.generate_setup_py(project_name))

        with open((project_path / "tox.ini").absolute(), "w") as tox_ini_file:
            tox_ini_file.write(self.tox_ini)

        return SUCCESS

