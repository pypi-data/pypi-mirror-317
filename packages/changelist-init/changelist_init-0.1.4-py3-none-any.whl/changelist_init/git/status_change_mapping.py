""" Maps Git Status data into FileChange data.
"""
from typing import Callable

from changelist_data.file_change import FileChange


def get_status_code_change_map(
    code: str,
) -> Callable[[str, ], FileChange]:
    """ Get a FileChange mapping callable for a specific code.

    Parameters:
    - code (str): The status code, determining what kind of FileChange (create, modify, delete)

    Returns:
    Callable[str, FileChange] - A function that maps a FileChange path into the FileChange object.
    """
    if code in ('M ', ' M', 'MM'):
        return lambda x: FileChange(before_path=x, before_dir=False, after_dir=False, after_path=x)
    if code in ('A ', ' A', 'AM', 'MA'):
        return lambda x: FileChange(after_dir=False, after_path=x)
    if code in ('D ', ' D', 'MD', 'DM'):
        return lambda x: FileChange(before_dir=False, before_path=x)
    if '?' in code or '!' in code:
        return lambda x: FileChange(after_dir=False, after_path=x)
    exit(f"Unknown Code: {code}")


def map_status_path_to_change(
    status_path: str,
) -> str:
    """ Convert Status File path to FileChange path.
        Adds a leading slash character.
    """
    return '/' + status_path if not status_path.startswith('/') else status_path


#GIT_FILE_STATUS_CODES = ["M", "T", "A", "D", "R", "C"]

#def decode_status_code(
#    code_char: str
#) -> str | None:
#    """ Return the English Keyword describing the Status of the file, given the Code.
#    """
#    match code_char:
#        case 'M', 'U':
#            return "Updated"
#        case 'T':
#            return "TypeChange"
#        case 'A':
#            return "Added"
#        case 'D':
#            return "Deleted"
#        case 'R':
#            return "Renamed"
#        case 'C':
#            return "Copied"
#        case '?':
#            return "Untracked"
#        case '!':
#            return "Ignored"
#    return None
