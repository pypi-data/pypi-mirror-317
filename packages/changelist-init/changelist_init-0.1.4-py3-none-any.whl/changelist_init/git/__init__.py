""" Git Management Package.
"""
from changelist_init.git.git_status_lists import GitStatusLists
from changelist_init.git import status_runner, status_reader


def get_status_lists(
    include_untracked: bool = False,
) -> GitStatusLists:
    """ Executes the Complete Git Status into File Change Operation.

    Returns:
    list[FileChange] - The List of FileChange information from Git Status.
    """
    return status_reader.read_git_status_output(
        status_runner.run_git_status() if not include_untracked else status_runner.run_untracked_status()
    )
