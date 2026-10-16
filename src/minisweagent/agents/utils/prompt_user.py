import sys
from typing import Any

from prompt_toolkit.formatted_text.html import HTML
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import PromptSession

from minisweagent import global_config_dir

try:  # prompt_toolkit's win32 backend can only be imported on Windows
    from prompt_toolkit.output.win32 import NoConsoleScreenBufferError
except (AssertionError, ImportError, AttributeError):
    NoConsoleScreenBufferError = ()  # type: ignore[assignment, misc]

_history = FileHistory(global_config_dir / "interactive_history.txt")


class _LazyPromptSession:
    """Prompt session that is created on first use.

    prompt_toolkit requires a console, so creating the session at import time would crash as soon as this module
    is imported without one (piped output, CI, or a Git Bash terminal on Windows). We then fall back to plain
    `input()` prompts, where multiline input is submitted with an empty line.
    """

    def __init__(self, *, multiline: bool = False, **kwargs: Any):
        self._multiline = multiline
        self._kwargs = kwargs
        self._session: PromptSession | None = None

    def prompt(self, message: str = "", **kwargs: Any) -> str:
        try:
            if self._session is None:
                self._session = PromptSession(history=_history, multiline=self._multiline, **self._kwargs)
            return self._session.prompt(message, **kwargs)
        except NoConsoleScreenBufferError:
            return self._fallback(message)

    def _fallback(self, message: str) -> str:
        if not self._multiline:
            return input(message)
        print("(multiline input, submit with an empty line)", file=sys.stderr)
        lines: list[str] = []
        while line := input(message if not lines else "> "):
            lines.append(line)
        return "\n".join(lines)


prompt_session = _LazyPromptSession()
_multiline_prompt_session = _LazyPromptSession(multiline=True)


def _multiline_prompt() -> str:
    return _multiline_prompt_session.prompt(
        "",
        bottom_toolbar=HTML(
            "Submit message: <b fg='yellow' bg='black'>Esc, then Enter</b> | "
            "Navigate history: <b fg='yellow' bg='black'>Arrow Up/Down</b> | "
            "Search history: <b fg='yellow' bg='black'>Ctrl+R</b>"
        ),
    )
