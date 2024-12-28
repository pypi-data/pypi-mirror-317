"""
Ruff tool handling
"""

import contextlib
from pathlib import Path

from nmk.model.builder import NmkTaskBuilder
from nmk.model.keys import NmkRootConfig
from nmk.utils import run_with_logs


class RuffBuilder(NmkTaskBuilder):
    """
    Ruff tool builder
    """

    def build(self, src_folders: list[str], command: str):
        """
        Invoke ruff

        :param src_folders: source folders to be analyzed
        :param command: ruff command to be executed
        """

        # Project folder
        project_folder = Path(self.model.config[NmkRootConfig.PROJECT_DIR].value)

        # Work with relative folders if needed
        relative_src_folders = []
        for f in src_folders:
            p = Path(f)
            with contextlib.suppress(ValueError):
                p = p.relative_to(project_folder)
            relative_src_folders.append(p)

        # Delegate to ruff
        run_with_logs(["ruff", command] + relative_src_folders, self.logger, cwd=project_folder)

        # Touch output file
        self.main_output.touch()
