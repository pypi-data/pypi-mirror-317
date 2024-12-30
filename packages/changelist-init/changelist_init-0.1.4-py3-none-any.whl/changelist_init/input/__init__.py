""" Input Sub-Package Methods.
"""
from pathlib import Path

from changelist_data.storage import load_storage
from changelist_data.storage.changelist_data_storage import ChangelistDataStorage
from changelist_data.storage.storage_type import StorageType

from changelist_init.input.argument_parser import parse_arguments
from changelist_init.input.input_data import InputData


def validate_input(
    arguments: list[str],
) -> InputData:
    """ Parse and Validate the Arguments, and return Input Data.
    """
    arg_data = parse_arguments(arguments)
    return InputData(
        storage=_determine_storage_type(
            arg_data.changelists_file,
            arg_data.workspace_file,
        ),
        include_untracked=arg_data.include_untracked,
    )


def _determine_storage_type(
    changelists_file: str | None,
    workspace_file: str | None,
) -> ChangelistDataStorage:
    # Check Path Args
    if changelists_file is not None:
        return load_storage(StorageType.CHANGELISTS, Path(changelists_file))
    if workspace_file is not None:
        return load_storage(StorageType.WORKSPACE, Path(workspace_file))
    # Search Default Paths
    return load_storage()
