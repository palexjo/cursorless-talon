from typing import Union
from ..paired_delimiter import paired_delimiters_map
from talon import Module, actions


mod = Module()

mod.list("cursorless_wrap_action", desc="Cursorless wrap action")


@mod.capture(
    rule=(
        "({user.cursorless_paired_delimiter} | {user.cursorless_wrapper_snippet}) {user.cursorless_wrap_action}"
    )
)
def cursorless_wrapper(m) -> Union[list[str], str]:
    try:
        paired_delimiter_info = paired_delimiters_map[m.cursorless_paired_delimiter]
        return {
            "action": "wrapWithPairedDelimiter",
            "extra_args": [paired_delimiter_info.left, paired_delimiter_info.right],
        }
    except AttributeError:
        return {
            "action": "wrapWithSnippet",
            "extra_args": [m.cursorless_wrapper_snippet],
        }


@mod.action_class
class Actions:
    def cursorless_wrap(cursorless_wrapper: dict, targets: dict):
        """Perform cursorless wrap action"""
        actions.user.cursorless_single_target_command_with_arg_list(
            cursorless_wrapper["action"], targets, cursorless_wrapper["extra_args"]
        )
