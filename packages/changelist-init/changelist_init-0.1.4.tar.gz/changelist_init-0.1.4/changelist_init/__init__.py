""" Changelist Init Package.
"""
from itertools import groupby
from typing import Generator, Iterable

from changelist_data.changelist import Changelist
from changelist_data.file_change import FileChange

from changelist_init.git import get_status_lists
from changelist_init.git.git_file_status import GitFileStatus
from changelist_init.git.status_change_mapping import get_status_code_change_map, map_status_path_to_change
from changelist_init.input import InputData


def initialize_file_changes(
    input_data: InputData,
) -> list[FileChange]:
    """ Get up-to-date File Change information in a list.
    """
    if input_data.include_untracked:
        file_status_generator = get_status_lists(True).merge_all()
    else:
        file_status_generator = get_status_lists(False).merge_tracked()
    return list(
        _map_file_status_to_changes(file_status_generator)
    )


def _map_file_status_to_changes(
    git_files: Iterable[GitFileStatus],
) -> Generator[FileChange, None, None]:
    """ Categorize by Status Code, and Map to FileChange data objects.

    Parameters:
    - git_files (Iterable[GitFileStatus]): An iterable or Generator providing GitFileStatus objects.

    Returns:
    FileChange - Yield by Generator.
    """
    for code, group in groupby(git_files, lambda w: w.code):
        mapping_function = get_status_code_change_map(code)
        for file_status in group:
            yield mapping_function(
                map_status_path_to_change(file_status.file_path)
            )


def merge_file_changes(
    existing_lists: list[Changelist],
    files: list[FileChange],
) -> bool:
    """ Carefully Merge FileChange into Changelists.
    """
    if (default_cl := _get_default_cl(existing_lists)) is not None:
        default_cl.changes.extend(
            _map_merge_fc(existing_lists, files)
        )
    else:
        existing_lists.append(
            Changelist('12345678', "Initial Changelist", files, "", True)
        )
    return True


def _map_merge_fc(
    changelists: list[Changelist],
    file_changes: list[FileChange],
) -> Generator[FileChange, None, None]:
    """ Merge FileChanges into existing Changelists using a map.
        Yields FileChange objects that were not mapped to an existing Changelist.

    Parameters:
    - existing_lists (list[Changelist]): The list of existing Changelists.
    - files (list[FileChange]): The list of FileChange objects produced during initialization.

    Returns:
    Generator[FileChange] - The FileChange objects that are new, not present in existing Changelists.
    """
    cl_map = _init_existing_fc_map(changelists)
    # Clear Existing Lists before merging new Files
    for cl in changelists:
        cl.changes.clear()
    # Search for matches using map
    for fc in file_changes:
        if not _map_fc_into_cl(cl_map, fc):
            yield fc


def _init_existing_fc_map(
    changelists: list[Changelist]
) -> dict[str, Changelist]:
    """ Initialize the Map of Existing FileChanges.

    Parameters:
    - changelists (list[Changelist]): The changelists to be inserted into the map.

    Returns:
    dict[str, Changelist] - A map from file path to the Changelist object that contains it.
    """
    cl_map = {}
    for cl in changelists:
        for fc in cl.changes:
            if (before := fc.before_path) is not None:
                cl_map[before] = cl
            if (after := fc.after_path) is not None:
                cl_map[after] = cl
    return cl_map


def _map_fc_into_cl(
    fc_map: dict[str, Changelist],
    file: FileChange
) -> bool:
    """ Map a FileChange into an existing Changelist.
    """
    if (before := file.before_path) is not None:
        if (cl := fc_map.get(before)) is not None: # Match!
            cl.changes.append(file)
            return True
    elif (after := file.after_path) is not None:
        if (cl := fc_map.get(after)) is not None: # Match!
            cl.changes.append(file)
            return True
    else:
        exit("This FC has no file path property.")
    # Fallthrough, the file path was not found in the map.
    return False


def _get_default_cl(
    lists: list[Changelist],
) -> Changelist | None:
    """ Find the Default Changelist, or set the first Changelist to default.
        Returns None if lists is empty.
    """
    if len(lists) > 0:
        for cl in lists:
            if cl.is_default:
                return cl
        # Return First list if no default attribute found
        return lists[0]
    return None
