from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any, ParamSpec, TypeVar

import click

_T = TypeVar("_T")
_P = ParamSpec("_P")
_EntryPoint = Callable[_P, _T]
ClickOption = Callable[[_EntryPoint[_P, _T]], _EntryPoint[_P, _T]]


RUN_ALL = "ALL"


def convert_choice(value: str, choices: Sequence[str]) -> list[str]:
    """Convert a choice to a list of choices, handling the special 'All' choice.

    Parameters
    ----------
    value
        The choice to convert.
    choices
        The set of choices to choose from.

    Returns
    -------
    list[str]
        The list of choices.
    """
    if value == RUN_ALL:
        return list(choices)
    return [value]


def process_choices(
    allow_all: bool,  # noqa: FBT001
    choices: Sequence[str] | None,
) -> tuple[click.ParamType, str | None, bool]:
    """Support function for creating options with choices.

    A common pattern in RRA pipelines is to build CLIs that admit a choice
    of a specific set of values or a special value that represents all
    possible values. This function provides a way to handle this pattern
    in a consistent way.

    There are four possible cases:
    1. No choices are provided and RUN_ALL is allowed. This is useful when the
        set of choices is not known ahead of time, or is contingent on another
        option. For example, if there is a task that depends on location and year,
        but the years available depend on the location. The user might want to
        run a single year for a location (which they'll have to know ahead of time);
        or all years for a location, which would be the subset of years available
        for that location; or all years for all locations, which could be a different
        subset of years for each included location.
    2. Choices are provided and RUN_ALL is allowed. This is useful when the set of
        choices is known ahead of time, but the user might want to run all of them.
    3. No choices are provided and RUN_ALL is not allowed. This is useful when the
        set of choices is not known ahead of time, but the user must provide a value.
    4. Choices are provided and RUN_ALL is not allowed. This is useful when the set of
        choices is known ahead of time and the user must provide a value.

    Parameters
    ----------
    allow_all
        Whether to allow the special value RUN_ALL.
    choices
        The set of choices to allow.

    Returns
    -------
    tuple[click.ParamType, str | None, bool]
        The option type, default value, and whether to show the default.
    """

    if choices is None:
        option_type: click.ParamType = click.STRING
        default = RUN_ALL if allow_all else None
    else:
        choices = list(choices)
        if allow_all:
            choices.append(RUN_ALL)
            default = RUN_ALL
        else:
            default = None
        option_type = click.Choice(choices)
    show_default = default is not None
    return option_type, default, show_default


def with_choice(
    name: str,
    short_name: str | None = None,
    *,
    allow_all: bool = True,
    choices: Sequence[str] | None = None,
    convert: bool | None = None,
    **kwargs: Any,
) -> ClickOption[_P, _T]:
    """Create an option with a set of choices.

    Parameters
    ----------
    name
        The name of the option.
    short_name
        An optional short name for the option.
    allow_all
        Whether to allow the special value "ALL", which represents all choices.
    choices
        The set of choices to allow.
    convert
        Whether to convert the provided argument to a list, resolving the special
        value "ALL" to all choices.

    """

    names = [f"--{name.replace('_', '-')}"]
    if short_name is not None:
        if len(short_name) != 1:
            msg = "Short names must be a single character."
            raise ValueError(msg)
        names.append(f"-{short_name}")
    option_type, default, show_default = process_choices(allow_all, choices)

    if convert is None:
        convert = allow_all

    if convert:
        if not allow_all:
            msg = "Conversion is only supported when allow_all is True."
            raise ValueError(msg)
        if choices is None:
            msg = "Conversion is only supported when choices are provided."
            raise ValueError(msg)

        def convert_to_list_callback(
            ctx: click.Context,  # noqa: ARG001
            param: click.Parameter,  # noqa: ARG001
            value: str,
        ) -> list[str]:
            return convert_choice(value, choices)

        kwargs["callback"] = convert_to_list_callback

    return click.option(
        *names,
        type=option_type,
        default=default,
        show_default=show_default,
        **kwargs,
    )


def with_verbose() -> ClickOption[_P, _T]:
    return click.option(
        "-v",
        "verbose",
        count=True,
        help="Configure logging verbosity.",
    )


def with_debugger() -> ClickOption[_P, _T]:
    return click.option(
        "--pdb",
        "debugger",
        is_flag=True,
        help="Drop into python debugger if an error occurs.",
    )


def with_input_directory(name: str, default: str | Path) -> ClickOption[_P, _T]:
    return click.option(
        f"--{name.replace('_', '-')}-dir",
        type=click.Path(exists=True, file_okay=False, dir_okay=True),
        default=default,
        show_default=True,
        help=f"Root directory where {name} inputs are stored.",
    )


def with_output_directory(default: str | Path) -> ClickOption[_P, _T]:
    return click.option(
        "--output-dir",
        "-o",
        type=click.Path(exists=True, file_okay=False, dir_okay=True),
        default=default,
        show_default=True,
        help="Root directory where outputs will be saved.",
    )


def with_num_cores(default: int) -> ClickOption[_P, _T]:
    return click.option(
        "--num-cores",
        "-c",
        type=click.INT,
        default=default,
        show_default=True,
    )


def with_queue() -> ClickOption[_P, _T]:
    return click.option(
        "-q",
        "queue",
        type=click.Choice(["all.q", "long.q"]),
        default="all.q",
        help="Queue to submit jobs to.",
    )


def with_progress_bar() -> ClickOption[_P, _T]:
    return click.option(
        "--progress-bar",
        "--pb",
        is_flag=True,
        help="Show a progress bar.",
    )


def with_dry_run() -> ClickOption[_P, _T]:
    return click.option(
        "--dry-run",
        "-n",
        is_flag=True,
        help="Don't actually run the workflow.",
    )


def with_overwrite() -> ClickOption[_P, _T]:
    return click.option(
        "--overwrite",
        is_flag=True,
        help="Overwrite existing files.",
    )
