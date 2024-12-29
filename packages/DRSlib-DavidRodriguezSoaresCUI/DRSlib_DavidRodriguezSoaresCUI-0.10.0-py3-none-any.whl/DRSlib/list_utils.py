"""
List utils
==========

Methods that perform simple but convenient operations,
specifically on lists
"""


def flatten_list(lst: list) -> list:
    """Flatten nested list"""
    if not any(isinstance(item, list) for item in lst):
        return lst

    res = []
    for item in lst:
        if isinstance(item, list):
            res.extend(flatten_list(item))
        else:
            res.append(item)
    return res
