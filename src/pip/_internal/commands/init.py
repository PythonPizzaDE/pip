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
    
    def add_options(self) -> None:
        self.cmd_opts.add_option("-f", "--folder", dest="target_dir", default=".",
                                 help="folder to initialize project in")

    def run(self, options: Values, args: List[str]) -> int:
        logger.verbose("Using %s", get_pip_version())
        project_path = pathlib.Path(options.target_dir)
        if not os.path.exists(project_path.absolute()):
            os.mkdir(project_path.absolute())
        return SUCCESS
