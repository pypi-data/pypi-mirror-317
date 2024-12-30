#!/usr/bin/python
from sys import argv, path


def main():
    # Have to import after appending parent dir to path
    from changelist_init.input import validate_input
    from changelist_init import initialize_file_changes, merge_file_changes
    #
    input_data = validate_input(argv[1:])
    cl = input_data.storage.get_changelists()
    if merge_file_changes(cl, initialize_file_changes(input_data)):
        # Successful Merge
        input_data.storage.update_changelists(cl)
        input_data.storage.write_to_storage()
    else:
        exit("Failed to Merge File Changes into Changelists")


if __name__ == "__main__":
    from pathlib import Path
    # Get the directory of the current file (__file__ is the path to the script being executed)
    current_directory = Path(__file__).resolve().parent.parent
    # Add the directory to sys.path
    path.append(str(current_directory))
    main()
