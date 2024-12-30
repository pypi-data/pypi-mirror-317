import os
import yaml
import json
import zipfile
import shutil
from typing import Union
from pathlib import Path
from glob import glob

import requests
from .exceptions import PathNotExists, NotYourType, NotGitHubUrl, ChiveError


def path_joiner(*paths):
    """
    Joins multiple path segments into a single Path object.

    Parameters:
    - *paths (str | Path): Path segments to join. These can be strings or Path objects.

    Returns:
    - Path: A Path object representing the joined path.

    Raises:
    - TypeError: If any of the provided paths is not a string or Path object.
    """

    combine_path = Path("/")
    for segment in paths:
        if not isinstance(segment, (str, Path)):
            raise TypeError(f"Invalid path segment type: {type(segment).__name__}. Expected str or Path.")
        combine_path = combine_path / Path(segment)

    return combine_path


def unzip(
        archive_file: Union[str, Path],
        parent_dir: Union[str, Path] = None,
        force_create: bool = True
):
    """
    Extracts the contents of a zip archive to the specified directory.

    Parameters:
    - archive_file (str | Path): The path to the zip archive file.
    - parent_dir (str | Path, optional): A parent directory to prepend to the output directory path.
    - force_create (bool, optional): If True, ensures the output directory is created even if it doesn't exist.
                                      (Not currently used but can be implemented for additional functionality.)

    Returns:
    - None
    """

    # Ensure `archive_file` is a Path object for consistent handling
    archive_path = Path(archive_file)

    # Determine the output directory name if not explicitly provided
    output_dir = archive_path.stem  # Use the filename without the extension

    # If a parent directory is specified, prepend it to the output directory
    if parent_dir:
        output_dir = Path(parent_dir) / output_dir

    # Create the output directory if it doesn't exist and `force_create` is True
    if force_create and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    # Open the zip archive and extract all files to the output directory
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

    print(f"Files successfully extracted to: {output_dir}")
    return output_dir


def is_github_url(url):
    if not url.startswith("https://github.com/"):
        raise NotGitHubUrl(url)

    if len(url.split("/")) != 5:
        raise NotGitHubUrl(url)

    return url


def url_joiner(base_url: str, *paths: str):
    """
    Joins a base URL with additional path segments, ensuring proper formatting.

    Parameters:
    - base_url (str): The base URL to which path segments will be appended.
    - *paths (str): Additional path segments to join to the base URL.

    Returns:
    - str: The combined URL with properly joined path segments.

    Raises:
    - TypeError: If `base_url` is not a string.
    """

    if not isinstance(base_url, str):
        raise TypeError(f"Expected a string for base_url, got {type(base_url).__name__} instead.")

    base_url = base_url.rstrip("/")

    for path_segment in paths:
        sanitize_segment = path_segment.strip("/") if isinstance(path_segment, str) else str(path_segment)
        base_url = f"{base_url}/{sanitize_segment}"

    return base_url


def url_lib_decoders(data: str):
    from urllib.parse import unquote
    return unquote(data)


def create_directory(directory_path: Path | str, force: bool = True):
    """
    Creates a directory with the option to create parent directories if they don't exist.

    Parameters:
    - directory (Path | str): The path of the directory to create. Can be a `Path` object or a string.
    - force (bool): If True, allows the creation of parent directories and avoids errors if the directory already exists.
                    Defaults to True.

    Returns:
    - None

    Raises:
    - ValueError: If the provided path is not a directory or is invalid.
    """

    directory = Path(directory_path)
    if directory.exists():
        if not directory.is_dir():
            raise ValueError(f"The path '{directory_path}' exists but is not a directory.")
        if not force:
            print(f"Directory '{directory_path}' already exists. Skipping creation.")
            return
    directory.mkdir(parents=force, exist_ok=True)


def extract_repo_path(repo_url):
    _repo_dir = repo_url.split("/")[4]
    if repo_url.endswith(".git"):
        _repo_dir = _repo_dir[:-4]
    return _repo_dir


def download_file(url, file_name, headers=None):
    """
    Download the file from the URL
    :param url:
    :type url:
    :param file_name:
    :type file_name:
    :param headers:
    :type headers:
    :return:
    :rtype:
    """
    with requests.get(url, headers=headers) as r:
        r.raise_for_status()
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return Path(file_name)


def load_json(file):
    with open(file) as f:
        data = json.load(f)
    return data


def load_yml(file) -> dict | list:
    with open(file) as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data


def _try_as(loader, data, on_error):
    """
    Tries to process the data with the given loader. Returns True if successful, False otherwise.
    """
    try:
        loader(data)
        return True
    except on_error:
        return False


def is_json(s):
    """
    Checks if the given data is valid JSON.
    """
    return _try_as(json.loads, s, json.JSONDecodeError)


def is_yaml(s):
    """
    Checks if the given data is valid YAML.
    """
    return _try_as(yaml.safe_load, s, yaml.YAMLError)


def load_config(file=None):
    if not os.path.exists(file):
        raise PathNotExists(file)

    if is_json(file):
        return load_json(file)

    elif is_yaml(file):
        return load_yml(file)

    return None


def load_env_vars(*vars):
    envs = {}
    for variable in vars:
        envs[variable] = os.environ.get(variable)

    return envs

def cleanup_file(regex: str | Path):
    """
    Remove the file / directory form the directory regex can also be passed with the glob
    Args:
        regex ():
    Returns:

    """
    if isinstance(regex, Path):
        regex = str(regex)

    files = glob(regex)
    for item in files:
        if os.path.isdir(item):
            shutil.rmtree(item)
        else:
            os.remove(item)
    return regex


def move_files(file_location, destination):
    """
    Move the file from one location to another using glob and shutil
    Args:
        file_location ():
        destination ():

    Returns:

    """
    files = glob(file_location)
    for file in files:
        shutil.move(file, destination)
    return destination

def basename(file: Path | str) -> str | Path:
    """
    Get the base name of a file path.

    This function returns the last component of the given file path. It supports both `Path` and `str` types.
    If the input is not of a supported type, it raises a `ChiveError`.

    Args:
        file (Union[Path, str]): The file path as a `Path` object or a string.

    Returns:
        Union[str, Path]: The base name of the file as a string if the input is a string,
                          or as a `Path` object if the input is a `Path`.

    Raises:
        ChiveError: If the input type is neither `Path` nor `str`.

    Examples:
        >>> basename(Path("/path/to/file.txt"))
        'file.txt'
        >>> basename("/path/to/file.txt")
        'file.txt'
        >>> basename(123)
        ChiveError: Unsupported type: <class 'int'>
    """
    if isinstance(file, Path):
        filename = file.name
        if not filename:
            raise ChiveError(f"The provided Path object '{file}' does not have a valid name.")
        return filename
    elif isinstance(file, str):
        base_name = os.path.basename(file)
        if not base_name:
            raise ChiveError(f"The provided string path '{file}' does not have a valid name.")
        return base_name
    else:
        raise ChiveError(f"Unsupported type: {type(file)}. Expected 'Path' or 'str'.")
