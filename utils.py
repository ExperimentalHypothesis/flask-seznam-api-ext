import os, time

# locked_paths = set()


# def authenticate(given_path: str) -> bool:
#     """ Check if particular paths (files/folders) can be requested via API. """
#     if given_path in locked_paths:
#         return False
#     else:
#         return True


def calculate_size(given_path: str) -> int:
    """ Get size of file/folder. """
    if os.path.isfile(given_path):
        return os.path.getsize(given_path)
    elif os.path.isdir(given_path):
        total = 0
        for path, dirs, folders in os.walk(given_path):
            for item in folders:
                if not os.path.islink(os.path.join(path, item)):
                    total += os.path.getsize(os.path.join(path, item))
        return total


def get_details(given_path: str) -> dict:
    """ Get detail info about a file/folder. """
    return {
        "path": given_path,
        "is_file": os.path.isfile(given_path),
        "size": calculate_size(given_path),
        "time_created": time.ctime(os.path.getctime(given_path)),
        "time_modified": time.ctime(os.path.getmtime(given_path)),
    }