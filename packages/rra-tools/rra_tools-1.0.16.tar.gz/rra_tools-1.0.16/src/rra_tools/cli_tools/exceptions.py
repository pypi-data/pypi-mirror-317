import functools
from bdb import BdbQuit
from collections.abc import Callable
from typing import ParamSpec, TypeVar

from rra_tools.logging import SupportsLogging

_T = TypeVar("_T")
_P = ParamSpec("_P")


def handle_exceptions(
    func: Callable[_P, _T],
    logger: SupportsLogging,
    *,
    with_debugger: bool,
) -> Callable[_P, _T]:
    """Drops a user into an interactive debugger if func raises an error."""

    @functools.wraps(func)
    def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> _T:  # type: ignore[return]
        try:
            return func(*args, **kwargs)
        except (BdbQuit, KeyboardInterrupt):
            raise
        except Exception:
            msg = "Uncaught exception"
            logger.exception(msg)
            if with_debugger:
                import pdb  # noqa: T100
                import traceback

                traceback.print_exc()
                pdb.post_mortem()
            else:
                raise

    return wrapped
