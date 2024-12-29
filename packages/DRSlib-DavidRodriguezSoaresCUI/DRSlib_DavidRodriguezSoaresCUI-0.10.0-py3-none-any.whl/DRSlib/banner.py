"""
Banner module
=============

Banners are text elements used in CLI interfaces. They use is
mostly for easthetic purposes. This module provides banner
generators and a wrapper (to bannerize functions/classes)

On formatters: two are provided
All formatters should have signature `(title: str, width: int = DEFAULT_BANNER_WIDTH, one_line: bool = False) -> str`
(or compatible) and (for formatters in banner.py) have an entry in global dictionnary `style_switch`.
"""

import functools
import shutil
from pathlib import Path
from typing import Any, Callable, Union

DEFAULT_BANNER_WIDTH = min(shutil.get_terminal_size().columns, 40)


def full_style_formatter(
    title: str, width: int = DEFAULT_BANNER_WIDTH, one_line: bool = False
) -> str:
    """Returns a "full style" banner in string representation"""
    title_len = len(title)
    padding = int((width - title_len - 2) / 2) * "#"
    title_spacing = " " if title_len % 2 == 1 else ""
    second_line = f"{padding} {title}{title_spacing} {padding}"

    return (
        second_line
        if one_line
        else "\n".join(["#" * width, second_line, "#" * width + "\n"])
    )


def lean_style_formatter(
    title: str, width: int = DEFAULT_BANNER_WIDTH, one_line: bool = False
) -> str:
    """Returns a "lean style" banner in string representation"""
    title_len = len(title)
    padding = int((width - title_len - 2) / 2) * " "
    title_spacing = " " if title_len % 2 == 1 else ""
    second_line = f"#{padding}{title}{title_spacing}{padding}#"

    return (
        second_line
        if one_line
        else "\n".join(["#" * width, second_line, "#" * width + "\n"])
    )


style_switch = {"full": full_style_formatter, "lean": lean_style_formatter}


def one_line_banner(
    title: str, style: Union[str, Callable] = "full", width: int = DEFAULT_BANNER_WIDTH
) -> str:
    """Returns a string containing a one-line banner
    Available styles : 'full', 'lean'
    External formatters: If style is Callable, it is assumed to be a formatter following
    signature norm (see module docstring)
    """

    style_formatter: Callable = style if callable(style) else style_switch[style]  # type: ignore[assignment]
    banner = style_formatter(title=title, width=width, one_line=True)
    return banner + "\n"


def multi_line_banner(
    title: str, style: Union[str, Callable] = "full", width: int = DEFAULT_BANNER_WIDTH
) -> str:
    """Returns a string containing a multi-line banner
    Available styles : 'full', 'lean'
    External formatters: If style is Callable, it is assumed to be a formatter following
    signature norm (see module docstring)
    """

    style_formatter: Callable = style if callable(style) else style_switch[style]  # type: ignore[assignment]
    banner = style_formatter(title=title, width=width)
    return banner + "\n"


def bannerize(
    style: Union[Callable, str],
    width: int = DEFAULT_BANNER_WIDTH,
    one_line: bool = False,
) -> Callable:
    """Decorator. Adds a banner before function's execution. Not intended nor tested for decorating classes.

    When `style` is given and is a callable formatter, it will be used to produce banner, otherwise `style`
    must be a string equal to a key in `style_switch`, which defines the formatter to use.

    Available styles : see style_switch
    """

    def actual_decorator(user_funtion: Callable) -> Callable:
        """Sets up the banner to be displayed for user_function"""
        nonlocal style_formatter, width, one_line  # type: ignore[misc]

        # Get name of the file containing `user_function`
        file_path = getattr(user_funtion.__globals__, "__file__")
        file_name = Path(file_path).stem
        # Setting the banner title
        _banner = style_formatter(
            title=file_name
            if user_funtion.__name__ == "main"
            else f"{file_name}.{user_funtion.__name__}",
            width=width,
            one_line=one_line,
        )

        @functools.wraps(user_funtion)
        def wrapper(*args, **kwargs) -> Any:
            """Prints the banner for user_function and executes it"""
            nonlocal _banner

            # Printing banner
            print(_banner)

            return user_funtion(*args, **kwargs)

        return wrapper

    style_formatter: Callable
    if callable(style):
        # formatter passed
        style_formatter = style
    elif isinstance(style, str):
        # `style` argument passed => validation
        try:
            style_formatter = style_switch[style]
        except KeyError as e:
            raise ValueError(
                f"bannerize: value for argument 'style' not recorgized: '{style}' not in {list(style_switch.keys())} !"
            ) from e
    else:
        raise ValueError(
            "bannerize: required value for 'style' is neither a formatter (Callable) nor a string."
        )

    return actual_decorator
