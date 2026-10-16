import locale
import os
import platform
import shutil
import signal
import subprocess
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from minisweagent.exceptions import Submitted
from minisweagent.utils.serialize import recursive_merge


class LocalEnvironmentConfig(BaseModel):
    cwd: str = ""
    env: dict[str, str] = {}
    timeout: int = 30
    interpreter: list[str] = []
    """Command used to interpret commands, e.g. ["bash", "-c"]. Empty (default) means the platform shell
    on POSIX and Git Bash (falling back to cmd.exe if Git is not installed) on Windows.
    Set it explicitly (e.g. ["cmd", "/c"]) to force a specific shell."""
    encoding: str = ""
    """Encoding used to decode command output. Empty (default) tries UTF-8 first, then the platform encoding."""


class LocalEnvironment:
    def __init__(self, *, config_class: type = LocalEnvironmentConfig, **kwargs):
        """This class executes commands directly on the local machine."""
        self.config = config_class(**kwargs)
        self.config.interpreter = self.config.interpreter or _default_interpreter()

    def execute(self, action: dict, cwd: str = "", *, timeout: int | None = None) -> dict[str, Any]:
        """Execute a command in the local environment and return the result as a dict."""
        command = action.get("command", "")
        cwd = cwd or self.config.cwd or os.getcwd()
        try:
            result = _run(
                command,
                cwd,
                _child_env(self.config.env),
                timeout or self.config.timeout,
                interpreter=self.config.interpreter,
                encoding=self.config.encoding,
            )
            output = {"output": result.stdout, "returncode": result.returncode, "exception_info": ""}
        except Exception as e:
            raw_output = getattr(e, "output", None)
            raw_output = (
                raw_output.decode("utf-8", errors="replace") if isinstance(raw_output, bytes) else (raw_output or "")
            )
            output = {
                "output": raw_output,
                "returncode": -1,
                "exception_info": f"An error occurred while executing the command: {e}",
                "extra": {"exception_type": type(e).__name__, "exception": str(e)},
            }
        self._check_finished(output)
        return output

    def _check_finished(self, output: dict):
        """Raises Submitted if the output indicates task completion."""
        lines = output.get("output", "").lstrip().splitlines(keepends=True)
        if lines and lines[0].strip() == "COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT" and output["returncode"] == 0:
            submission = "".join(lines[1:])
            raise Submitted(
                {
                    "role": "exit",
                    "content": submission,
                    "extra": {"exit_status": "Submitted", "submission": submission},
                }
            )

    def get_template_vars(self, **kwargs) -> dict[str, Any]:
        return recursive_merge(self.config.model_dump(), platform.uname()._asdict(), os.environ, kwargs)

    def serialize(self) -> dict:
        return {
            "info": {
                "config": {
                    "environment": self.config.model_dump(mode="json"),
                    "environment_type": f"{self.__class__.__module__}.{self.__class__.__name__}",
                }
            }
        }


def _default_interpreter() -> list[str]:
    """Use Git Bash on Windows, because the agent's prompts assume a POSIX shell."""
    if os.name != "nt" or not (bash := _find_git_bash()):
        return []
    return [bash, "-c"]


def _find_git_bash() -> str | None:
    """Find a native Git Bash, skipping the WSL shim (which would run commands in a different filesystem)."""
    local_app_data = os.getenv("LOCALAPPDATA")
    # Fall back to the default install locations, because the environment might be stripped down
    roots = [
        os.getenv("ProgramFiles") or r"C:\Program Files",
        os.getenv("ProgramFiles(x86)") or r"C:\Program Files (x86)",
        f"{local_app_data}\\Programs" if local_app_data else "",
    ]
    candidates = [Path(root) / "Git" / "bin" / "bash.exe" for root in roots if root]
    if from_path := shutil.which("bash"):
        candidates.append(Path(from_path))
    return next((str(path) for path in candidates if path.is_file() and not _is_wsl_shim(path)), None)


def _is_wsl_shim(path: Path) -> bool:
    return path.name.lower() == "bash.exe" and any(part.lower() in {"system32", "windowsapps"} for part in path.parts)


def _child_env(configured: dict[str, str]) -> dict[str, str]:
    env = os.environ | configured
    if os.name == "nt":
        # Windows programs otherwise write in the legacy codepage (e.g. cp936), which we cannot decode
        env.setdefault("PYTHONUTF8", "1")
        env.setdefault("PYTHONIOENCODING", "utf-8")
    return env


def _decode(raw: bytes, encoding: str = "") -> str:
    """Decode command output, preferring UTF-8 (as on Linux) and falling back to the platform encoding."""
    for candidate in (encoding or "utf-8", "mbcs" if os.name == "nt" else locale.getpreferredencoding(False)):
        try:
            return _normalize_newlines(raw.decode(candidate))
        except (UnicodeDecodeError, LookupError):
            continue
    return _normalize_newlines(raw.decode("utf-8", errors="replace"))


def _normalize_newlines(text: str) -> str:
    """Translate CRLF/CR to LF, the way subprocess' text mode does."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _run(
    command: str,
    cwd: str,
    env: dict[str, str],
    timeout: int,
    interpreter: list[str] | None = None,
    encoding: str = "",
) -> subprocess.CompletedProcess[str]:
    """Like subprocess.run, but kills the whole process group on timeout so no children are orphaned."""
    process = subprocess.Popen(
        [*interpreter, command] if interpreter else command,
        shell=not interpreter,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=os.name == "posix",
    )
    try:
        stdout, _ = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL) if os.name == "posix" else process.kill()
        stdout, _ = process.communicate()
        raise subprocess.TimeoutExpired(command, timeout, output=_decode(stdout, encoding))
    return subprocess.CompletedProcess(command, process.returncode, stdout=_decode(stdout, encoding))
