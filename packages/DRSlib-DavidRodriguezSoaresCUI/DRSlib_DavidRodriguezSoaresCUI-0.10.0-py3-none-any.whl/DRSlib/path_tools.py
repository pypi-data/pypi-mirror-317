# pylint: disable=too-few-public-methods, import-error, wrong-import-order, broad-except


"""
Path tools
==========

Easy to use tool to collect files matching a pattern.

Note: both class and function versions should be euivalent, both kept
just in case. Class may be usefull for repeated calls to `collect` method.

"""

import logging
import re
import sys
from os import popen
from pathlib import Path
from shutil import copy2
from typing import List, Optional, Tuple, Union

from send2trash import send2trash

from .execute import execute
from .os_detect import Os
from .utils import assertTrue

LOG = logging.getLogger(__file__)
MAKE_FS_SAFE_PATTERN = re.compile(pattern=r'[\\/*?:"<>|]')
FILESYSTEM_SAFE_CHARACTER_MAP = {
    "<": "﹤",
    ">": "﹥",
    ":": "ː",
    '"': "“",
    "/": "⁄",
    "\\": "∖",
    "|": "⼁",
    "?": "？",
    "*": "﹡",
    ".": "․",
}
FS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
}

try:
    import win32api
except ImportError:
    current_os = Os()
    if current_os.windows:
        LOG.warning("Could not import optional dependency win32api; This shou")


class FileCollector:
    """Easy to use tool to collect files matching a pattern (recursive or not), using pathlib.glob.
    Reasoning for making it a class: Making cohexist an initial check/processing on root with a recursive
    main function was not straightforward. I did it anyway, so feel free to use the function alternative.
    """

    def __init__(self, root: Path) -> None:
        assertTrue(root.is_dir(), "Root dir must exist: '{}'", root)
        root.resolve()
        self.root = root
        self.log = logging.getLogger(__file__)
        self.log.debug("root=%s", root)

    def collect(self, pattern: str = "**/*.*") -> List[Path]:
        """Collect files matching given pattern(s)"""
        files = []

        # 11/11/2020 BUGFIX : was collecting files in trash like a cyber racoon
        files = [
            item.resolve()
            for item in self.root.glob(pattern)
            if item.is_file() and ("$RECYCLE.BIN" not in item.parts)
        ]

        self.log.debug("\t'%s': Found %s files in %s", pattern, len(files), self.root)

        return files


def file_collector(root: Path, pattern: str = "**/*.*") -> List[Path]:
    """Easy to use tool to collect files matching a pattern (recursive or not), using pathlib.glob.
    Collect files matching given pattern(s)"""
    assertTrue(root.is_dir(), "Root dir must exist: '{}'", root)
    root.resolve()
    LOG.debug("root=%s", root)

    def collect(_pattern: str) -> List[Path]:
        # 11/11/2020 BUGFIX : was collecting files in trash like a cyber racoon
        _files = [
            item
            for item in root.glob(_pattern)
            if item.is_file() and ("$RECYCLE.BIN" not in item.parts)
        ]
        LOG.debug("\t'%s': Found %s files in %s", _pattern, len(_files), root)
        return _files

    files = collect(pattern)

    return files


def make_FS_safe(s: str, mode: str = "strip", len_limit: int = 200) -> str:
    """File Systems don't accept all characters on file/directory names. This
    function tries to make a file name that is acceptable for Windows and Linux systems.
    Do not use this function on file names that include extension.

    `mode`: how to deal with a selection of illegal characters:
     - 'strip': remove illegal characters
     - 'utf-replace': replace illegal characters with similar utf characters

    `len_limit`: cut name so it's not too long and adds '…' at the end to mark the cut

    Note: on all modes, non-printable ASCII characters are removed
    """
    # remove non-printable ASCII characters
    res = "".join(c for c in s if ord(c) >= 32)

    # deal with some special characters
    if mode == "strip":
        res = re.sub(pattern=MAKE_FS_SAFE_PATTERN, repl="", string=res)
    elif mode == "utf-replace":
        res = "".join(FILESYSTEM_SAFE_CHARACTER_MAP.get(c, c) for c in res)
    else:
        raise ValueError(f"Unknown mode '{mode}'")

    # Shorten name
    res = res[: len_limit - 1] + "…" if len(res) > len_limit else res

    # Avoid reserved names by adding a small suffix
    if res in FS_RESERVED_NAMES:
        res += "_"

    return res


def find_available_path(
    root: Path, base_name: str, file: bool = True, file_ext: str = ""
) -> Path:
    """Returns a path to a file/directory that DOESN'T already exist.
    The file/dir the user wishes to make a path for is referred as X.

    `root`: where X must be created. Can be a list of path parts

    `base_name`: the base name for X. May be completed with '(index)' if name already exists.

    `file`: True if X is a file, False if it is a directory
    """

    # Helper function: makes suffixes for already existing files/directories
    def suffixes():
        yield ""
        idx = 0
        while True:
            idx += 1
            yield f" ({idx})"

    # Iterate over candidate paths until an unused one is found
    safe_base_name = make_FS_safe(base_name, len_limit=len(base_name))
    if file:
        for suffix in suffixes():
            _object = root / (safe_base_name + suffix + file_ext)
            if not _object.is_file():
                return _object
    else:
        for suffix in suffixes():
            _object = root / (safe_base_name + suffix)
            if not _object.is_dir():
                return _object

    raise RuntimeError("Failed to find an available path")


def make_valid_path(
    root: Union[Path, List], base_name: str, file: bool = True, create: bool = False
) -> Path:
    """Returns a path to a file/directory that DOESN'T already exist.
    The file/dir the user wishes to make a path for is referred as X.

    `root`: where X must be created. Can be a list of path parts
    `base_name`: the base name for X. May be completed with '(index)' if name already exists.
    `file`: True if X is a file, False if it is a directory
    `create`: True instantiates X (empty file or dir), False doesn't

    Build upon `find_available_path`, adding:

    - root path construction (List->Path)

    - root mkdir

    - ability to initialize returned file/dir

    """

    # make root path
    if isinstance(root, List):
        if isinstance(root[0], str):
            _root = Path(make_FS_safe(root[0]))
        elif isinstance(root[0], Path):
            _root = root[0]
        else:
            raise TypeError(
                f"root[0]={root[0]} is of unexpected type {type(root[0])}, not str or Path !"
            )

        for path_part in root[1:]:
            assertTrue(
                isinstance(path_part, str),
                "path part in root '{}' is of unexpected type {}, not str !",
                path_part,
                type(path_part),
            )
            safe_path_part = make_FS_safe(path_part)
            assertTrue(
                safe_path_part is not None,
                "make_FS_safe returned None for '{}'",
                path_part,
            )
            _root = _root / safe_path_part
    elif isinstance(root, Path):
        _root = root
    else:
        raise TypeError(
            f"root={root} is of unexpected type {type(root)}, not str or Path !"
        )

    # make root directory
    ensure_dir_exists(_root)

    # Find valid path
    valid_path = find_available_path(_root, base_name, file)

    # Optionally create file/dir
    if create:
        if file:
            valid_path.touch()
        else:
            valid_path.mkdir()

    return valid_path


def ensure_dir_exists(folder: Path) -> None:
    """Tests whether `folder` exists, creates it (and its whole path) if it doesn't."""
    if folder.is_file():
        raise ValueError(f"Given path '{folder}' is a file !")
    if not folder.is_dir():
        folder.mkdir(parents=True)


def folder_get_file_count(_root: Path, use_fallback: bool = False) -> int:
    """Uses built-in platform-specific ways to recursively count the number of files in a given directory.
    Reason for using CLI calls to platform-specific external tools : they typically offer superior performance (because optimised)

    `use_fallback` : if True, use Path.glob instead of platform-specific CLI calls (mainly for testing puposes)
    """
    _root = _root.resolve()

    def fallback() -> int:
        return sum(1 for x in _root.glob("**/*") if x.is_file())

    if use_fallback:
        return fallback()

    _current_os = Os()
    command = None
    if _current_os.windows:
        # Windows CMD
        LOG.debug("Crawler from '%s'", _root)
        command = f'dir "{_root}" /A:-D /B /S | find "." /C'
    elif _current_os.wsl or _current_os.linux:
        # Linux
        LOG.debug("Crawler from '%s'", _root)
        command = f'find "{_root}" -type f|wc -l'
    else:
        LOG.warning(
            "OS not recognised or has no specific command set (%s); fallback method used.",
            _current_os,
        )
        return fallback()

    return int(popen(command).read().strip())  # nosec B605


def folder_get_subdirs(root_dir: Path) -> List[Path]:
    """Return a list of first level subdirectories"""
    assertTrue(root_dir.is_dir(), "Root dir must exist: '{}'", root_dir)
    return [
        item
        for item in root_dir.resolve().iterdir()
        if item.is_dir() and ("$RECYCLE.BIN" not in item.parts)
    ]


def windows_list_logical_drives() -> List[Path]:
    """Uses windows-specific methods to retrieve a list of logical drives.

    Both methods have been developped and tested to give equivalent output and be interchangeable

    Warning: Only works on Windows !
    """

    def method1():
        """uses a windows shell command to list drives"""

        def filter_drives(lst):
            for item in lst:
                if not item:
                    continue
                try:
                    yield Path(item).resolve()
                except Exception:  # nosec B112
                    continue

        drives = list(filter_drives(win32api.GetLogicalDriveStrings().split("\x00")))
        return drives

    def method2():
        """uses a windows shell command to list drives"""
        command = ["wmic", "logicaldisk", "get", "name"]
        stdout = execute(command)["stdout"]

        def return_cleaned(lst):
            for item in lst:
                if len(item) < 2:
                    continue
                if item[0].isupper() and item[1] == ":":
                    try:
                        # Bugfix : the '<driveletter>:' format was resolving to CWD when driveletter==CWD's driveletter.
                        # This seems to be an expected Windows behavior. Fix: switch to '<driveletter>:\\' format, which is more appropriate.
                        yield Path(item[:2] + "\\").resolve()
                    except Exception:  # nosec B112
                        continue

        drives = list(return_cleaned(stdout.splitlines()))
        return drives

    try:
        return method1()
    except Exception:
        try:
            return method2()
        except Exception as e:
            LOG.error("windows_list_logical_drives: something went wrong: %s", e)
            sys.exit(1)


def safe_file_copy(
    file: Path,
    destination_dir: Path,
    file_size: Optional[int] = None,
    rename_if_destination_exists: bool = False,
) -> Tuple[Optional[Path], int]:
    """Copies file to some directory, and returns the destination file path and the amount of bytes copied.
    If target file already exists, nothing is copied (content is not verified for a match).

    Note: Can fail if:

    * source file doesn't exist

    * target file exists and ``rename_if_destination_exists=False``

    * shutils.copy2 fails (out of space error or other).

    `file_size`: File size in bytes. If provided, avoids a call to check the actual file size.

    `rename_if_destination_exists`: Instead of failing if a file with same name already exist in destination
    directory, choose an alternative name instead (add ' (1)' or similar at the end of the name)

    Returns: Tuple (<target_file_path:Path|None>, <copied_bytes:int>)
    """
    assertTrue(
        file is not None and file.is_file(),
        "Argument error: File None or non-existing: '{}'",
        file,
    )

    # Making target path
    target = destination_dir / file.name
    if target.exists():
        if rename_if_destination_exists:
            target = find_available_path(
                root=destination_dir, base_name=file.name, file=True
            )
        else:
            LOG.warning(
                "Cannot copy %s because target already exist : %s", file.name, target
            )
            return (None, 0)

    # Copy
    LOG.info("Copying %s -> %s", file, target)
    copy2(file, target)
    LOG.info("Copying done !")

    return (target, file_size if file_size else file.stat().st_size)


def replace_file(to_be_replaced: Path, replacing: Path) -> None:
    """Tries to replace a file by another. Sends both ``to_be_replaced`` file
    and original ``replacing`` file to trash.
    """
    assertTrue(
        to_be_replaced.is_file(), "File to be replaced must exist: '{}'", to_be_replaced
    )
    assertTrue(
        replacing.is_file(),
        "File replacing file to be replaced must exist: '{}'",
        replacing,
    )

    LOG.info("Sending '%s' to trash", to_be_replaced)
    send2trash(to_be_replaced)

    LOG.info("Replacing file %s by file at %s", to_be_replaced, replacing)
    bytes_to_move = replacing.stat().st_size
    _, bytes_copied = safe_file_copy(
        file=replacing, destination_dir=to_be_replaced.parent
    )
    if bytes_copied != bytes_to_move:
        LOG.warning(
            "Something went wrong while copying: bytes_copied=%d != %d=bytes_to_move",
            bytes_copied,
            bytes_to_move,
        )
        return

    LOG.info("Sending '%s' to trash", replacing)
    send2trash(replacing)


def open_folder_in_explorer(directory: Path) -> None:
    """Tries to open a file explorer window to given directory

    Note: as of now, only the windows-specific part was tested,
    not WSL or linux
    """
    directory_s = str(directory.resolve())
    _os = Os()
    if _os.windows or _os.cygwin or _os.wsl:
        command = ["explorer.exe", directory_s.replace("\\" * 2, "\\")]
    elif _os.linux:
        command = ["xdg-open", directory_s]
    else:
        LOG.warning("Unsupported OS platform '%s' !", _os)
        return

    LOG.debug("executing command: '%s'", command)
    execute(command)
