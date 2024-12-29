# pylint: disable=too-many-return-statements
"""
String-focused utils
====================

Simple utils that accomplish one task well, specifically string operations.

"""

import re

DOUBLE_QUOTE = '"'
SI_SUFFIX = {"K": 1_000, "M": 1_000_000, "G": 1_000_000_000}


def ensure_quoted_on_space(s: str) -> str:
    """Ensures a string containing spaces is fully enclosed
    between double quotes
    """
    if " " not in s:
        return s
    return ensure_double_quotes(s)


def ensure_double_quotes(s: str) -> str:
    """Ensures s is double quoted in a particular way :
     - returned string must begin and end with a double quote character `"`
     - any double quote that isn't at the beginning or end must be escaped `\\"`

    Examples :
     - `` (empty string) -> `""`
     - `.` -> `"."`
     - `hello` -> `"hello"`
     - `"hello` -> `"hello"`
     - `hello"` -> `"hello"`
     - `"hello"` -> `"hello"` (unchanged)
     - `"he"llo` -> `"he\\"llo"`
     - `"he\\"llo"` -> `"he\\"llo"` (unchanged)

    """

    if not s:
        return '""'
    if len(s) == 1:
        if s[0] == '"':
            return '"\\""'
        return '"' + s + '"'
    # else
    if s[0] != '"':
        return ensure_double_quotes('"' + s)
    if s[-1] != '"':
        return ensure_double_quotes(s + '"')

    # past this point, 2 <= len(s) and there are double quotes at the beginning and end of s.

    double_quote_locations = set(m.start() for m in re.finditer(r'"', s))
    escaped_double_quote_locations = set(m.start() + 1 for m in re.finditer(r'\\"', s))
    double_quote_locations.difference_update(escaped_double_quote_locations)

    # s lacks any double quotes
    if not double_quote_locations:
        return '"' + s + '"'

    # detection of double quotes to escape
    proper_double_quote_location = set([0, len(s) - 1])
    misplaced_double_quotes = set(double_quote_locations).difference(
        proper_double_quote_location
    )
    # print(f"proper_double_quote_location={proper_double_quote_location}")
    # print(f"double_quote_locations={double_quote_locations}")
    # print(f"misplaced_double_quotes={misplaced_double_quotes}")

    # s is already properly double quoted
    if not misplaced_double_quotes:
        return s

    # escaping double quotes plus recursion
    s_characters = list(s)
    misplaced_DQ_idx = misplaced_double_quotes.pop()
    _s = "".join(
        s_characters[:misplaced_DQ_idx]
        + ["\\", '"']
        + s_characters[misplaced_DQ_idx + 1 :]
    )
    return ensure_double_quotes(_s)


def truncate_str(s: str, output_length: int, cut_location: str = "center") -> str:
    """Truncates string to a new length

    `cut_location` : (default:'center') in ['left','center','right']
    """
    s_len = len(s)
    if s_len <= output_length:
        return s
    if output_length <= 7:
        print(
            f"Warning: used truncate_str with 'output_length'={output_length}<=7, which is too low and would probably result in undesired results, so 's' was returned unchanged !"
        )
        return s

    # len_diff = s_len-output_length
    if cut_location == "left":
        return f"{s[:output_length-6]} [...]"
    if cut_location == "center":
        offset = (output_length // 2) - 3
        return f"{s[:offset]} [...] {s[-(offset - (1 if output_length%2==0 else 0)):]}"

    if cut_location == "right":
        return f"[...] {s[-(output_length-6):]}"
    # else
    raise ValueError(
        f"truncate_str: given parameter 'cut_location'={cut_location} is not in ['left','center','right'] !"
    )


def human_parse_int(s: str) -> int | str:
    """Decodes values such as:
    - 12.5k => 12500
    - -44G => -44000000
    Returns int on success, str on failure
    """
    if len(s) < 1:
        return s
    if len(s) > 1 and (suffix := s[-1].upper()) in SI_SUFFIX:
        try:
            base_value = float(s[:-1])
            return int(base_value * SI_SUFFIX[suffix])
        except ValueError:
            return s
    try:
        return int(s)
    except ValueError:
        return s
