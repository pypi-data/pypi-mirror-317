
import re
from typing import Any, Optional

def filter_framedict(
    framedict: dict[str, Any],
    selected_keys: Optional[set[str]] = None
) -> dict[str, Any]:
    """
    Filters only selected keys we wish to display from framedict

    Args:
        framedict (dict[str, Any]): dict containing variables we get from FrameType.f_locals
        selected_keys (Optional[set[str]]): user-selected keys they wish to keep track of.

    Returns:
        (dict[str, Any]): filtered dict
    """
    if selected_keys:
        # if user has entered selected keys, limit framedict only to selected keys
        framedict: dict[str, Any] = {
            key: value 
            for key, value in framedict.items()
            if key in selected_keys
        }
    else:
        # if user leave it blank, assume they want everything. simply remove keys starting with _
        framedict: dict[str, Any] = {
            key: value
            for key, value in framedict.items()
            if str(key)[0] != "_"
        }

    # remove key-value pairs with non-informative values eg. <something object at abcdefg>
    return {
        key: value
        for key, value in framedict.items()
        if not re.match(r"<.*>", str(value))
    }

def compute_diff(
    current_framedict: dict[str, Any],
    new_framedict: dict[str, Any],
) -> dict[str, Any]:
    """
    Extract only changed values in new_framedict (compared to current_framedict)

    Args:
        current_framedict (dict[str, Any]): existing variables in previous frame
        new_framedict (dict[str, Any]): new variables in new frame

    Returns:
        (dict[str, Any]): dict containing only key-value pairs in new_framedict where
            1) key not in current_framedict (new variable created)
            2) value not equal to the one in current_framedict (variable reassigned or mutated)
    """
    return {
        key: value
        for key, value in new_framedict.items()
        if (
            key not in current_framedict
            or value != current_framedict[key]
        )
    }