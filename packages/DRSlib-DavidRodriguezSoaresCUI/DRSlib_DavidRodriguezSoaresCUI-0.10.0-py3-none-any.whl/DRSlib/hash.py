"""
Hash-related tools
==================

Useful tools for easily hashing files. See crctools.utils for more functions.
"""

import hashlib
import logging
import zlib
from pathlib import Path
from typing import Dict, Optional

from .os_detect import Os
from .path_tools import ensure_dir_exists, file_collector
from .spinner import MySpinner
from .utils import assertTrue, pickle_this, unpickle_this

BLOCKSIZE = 65_536  # 2 ** 16
log = logging.getLogger(__file__)
spinner = MySpinner()
current_os = Os()


def file_hash(file: Path) -> str:
    """Returns the md5 hash of the corresponding file
    Reads the file in 2^16 bytes (~65Ko) chunks
    """

    hasher = hashlib.md5()  # nosec B324
    with file.open(mode="rb") as f:
        chunk = f.read(BLOCKSIZE)
        while 0 < len(chunk):
            hasher.update(chunk)
            chunk = f.read(BLOCKSIZE)

    hash_s = hasher.hexdigest()

    log.debug("File %s has md5 hash %s.", file, hash_s)
    return hash_s


def partial_MD5(file: Path) -> str:
    """Reads up to 10MB of the given file and returns MD5 (partial) checksum. Borrowing code from : https://stackoverflow.com/a/1131238
    This is achieved by reading 10 times ~1MB, thus reducing RAM usage.
    """
    hasher = hashlib.md5()  # nosec B324
    with file.open(mode="rb") as f:
        for _ in range(10):
            chunk = f.read(1_048_576)
            if not chunk:
                break
            hasher.update(chunk)

    return hasher.hexdigest()


def path_to_id(_path: Path, limit_id_len: bool = True) -> str:
    """Returns a string identifier for any given file/directory path.

    `limit_id_len`: If True, keeps id length below 190 characters
    """
    path = _path.resolve()

    anchor_len = 3 if current_os.wsl else len(path.anchor)

    _id = str(path)[anchor_len:]
    if limit_id_len and 190 < len(_id):
        _id = _id[:160] + " [...] " + _id[-20:]

    return _id


def directory_hash(
    directory: Path,
    pattern: str = "*.*",
    old_hashes: Optional[dict] = None,
) -> Dict[str, str]:
    """Returns a dictionnary of md5 hash of all the files in the directory
    corresponding to path 'directory'.

    Returns: Dict[<file_name:str>, <file_hash:str>]
    """

    files = file_collector(root=directory, pattern=pattern)
    if old_hashes is None:
        old_hashes = {}

    hashes = {}
    for file in files:
        key = file.name
        if key in old_hashes:
            log.debug("Cache hit")
            hashes[key] = old_hashes[key]
            continue

        hashes[key] = file_hash(file)

    return hashes


def tree_hash(
    root: Path,
    hash_location: Path,
    pattern: str = "*.*",
    fastload: bool = False,
) -> None:
    """Explores the directory structure recursively from 'root', computing their hash.
    For each directory explored, saves hashes found to a file.

    `fastload`: If True and the corresponding hash file is found, hashes are not re-checked. This
    is used for performance reasons. Do not use if changes are likely.

    """

    root = root.resolve()
    hash_location = hash_location.resolve()
    assertTrue(root.is_dir(), "Root dir must exist: '{}'", root)
    ensure_dir_exists(hash_location)

    subdirectories = [x for x in root.iterdir() if x.is_dir() and x != hash_location]
    for sub_dir in subdirectories:
        savefile = hash_location / path_to_id(sub_dir)

        if not (fastload and savefile.is_file()):
            old_hashes = unpickle_this(savefile)
            spinner.animation()
            hashes = directory_hash(
                directory=sub_dir, pattern=pattern, old_hashes=old_hashes
            )
            data = {"folder": sub_dir, "hashes": hashes}

            pickle_this(data, savefile)
        else:
            spinner.animation(text="cache hit")

        # Recursion
        tree_hash(
            root=sub_dir,
            hash_location=hash_location,
            pattern=pattern,
            fastload=fastload,
        )


def get_temporary_dir_name(file: Path) -> str:
    """Returns predictable (approximately) unique 8-character (uppercase hexadecimal
    alphanumeric) name, typically used for temporary directories"""
    return hex(zlib.crc32(file.name.encode(encoding="utf8")))[2:].upper()
