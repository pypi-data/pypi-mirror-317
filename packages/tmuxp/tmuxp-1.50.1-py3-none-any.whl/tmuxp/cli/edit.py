"""CLI for ``tmuxp edit`` subcommand."""

import argparse
import os
import pathlib
import subprocess
import typing as t

from tmuxp.workspace.finders import find_workspace_file


def create_edit_subparser(
    parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:
    """Augment :class:`argparse.ArgumentParser` with ``edit`` subcommand."""
    parser.add_argument(
        dest="workspace_file",
        metavar="workspace-file",
        type=str,
        help="checks current tmuxp and current directory for workspace files.",
    )
    return parser


def command_edit(
    workspace_file: t.Union[str, pathlib.Path],
    parser: t.Optional[argparse.ArgumentParser] = None,
) -> None:
    """Entrypoint for ``tmuxp edit``, open tmuxp workspace file in system editor."""
    workspace_file = find_workspace_file(workspace_file)

    sys_editor = os.environ.get("EDITOR", "vim")
    subprocess.call([sys_editor, workspace_file])
