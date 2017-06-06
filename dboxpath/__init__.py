"""Provide utility function to get Dropbox root directory path."""
import os
import json


def get_db_path():
    """Return the path to Dropbox's info.json file with user-settings."""
    if os.name == 'posix':  # OSX-specific
        home_path = os.path.expanduser('~')
        dbox_db_path = os.path.join(home_path, '.dropbox', 'info.json')

    elif os.name == 'nt':  # Windows-specific
        home_path = os.getenv('LOCALAPPDATA')
        dbox_db_path = os.path.join(home_path, 'Dropbox', 'info.json')

    else:
        raise NotImplementedError("Unknown Platform: {0}".format(os.name))

    return dbox_db_path


def get_root():
    """Return the path to root directory of Dropbox."""

    db_path = get_db_path()
    try:
        with open(db_path) as data_file:
            dbox_db = json.load(data_file)
            dbox_path = dbox_db['personal']['path']
    except FileNotFoundError:
        raise FileNotFoundError("Unable to locate Dropbox database file.")

    return dbox_path


def get_path(*subdirectories):
    """Return an absolute path to a Dropbox subdirectory."""

    dbox_path = get_root()

    if not subdirectories:
        return dbox_path

    # subdirectories passed in, check if that path exists
    sub_path = os.path.join(dbox_path, *subdirectories)

    if not os.path.exists(sub_path):
        raise IOError("Path does not exist: {0}".format(sub_path))
    else:
        return sub_path
