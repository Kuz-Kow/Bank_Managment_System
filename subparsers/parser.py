import argparse
import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated, Any, get_args, get_origin, get_type_hints


ParserCommand = Callable[..., Any]


@dataclass(frozen=True)
class ParserArgument:
    """Describe one CLI argument derived from a command parameter."""

    name: str
    argument_type: Any
    description: str | None
    choices: list[Any] | tuple[Any, ...] | None
    default: Any


@dataclass(frozen=True)
class ParserCommandSpec:
    """Pair a registered command with its parsed argument metadata."""

    function: ParserCommand
    arguments: tuple[ParserArgument, ...]


PARSERS: dict[str, ParserCommandSpec] = {}


def addparser(function: ParserCommand) -> ParserCommand:
    """Register a command and derive its CLI arguments from its signature."""
    command_name = "-".join(function.__name__.split("_"))
    if command_name in PARSERS:
        raise ValueError(f"Parser command '{command_name}' is already registered")

    parameters = list(inspect.signature(function).parameters.values())
    if not parameters:
        raise TypeError(f"Parser command '{command_name}' must accept the database argument")

    hints = get_type_hints(function, include_extras=True)
    arguments: list[ParserArgument] = []
    for parameter in parameters[1:]:
        annotation = hints.get(parameter.name, parameter.annotation)
        if get_origin(annotation) is Annotated:
            argument_type, *metadata = get_args(annotation)
        else:
            argument_type, metadata = annotation, []

        if argument_type is inspect.Parameter.empty:
            raise TypeError(
                f"Parser argument '{parameter.name}' for '{command_name}' must be annotated"
            )

        description = metadata[0] if metadata and isinstance(metadata[0], str) else None
        choices = next(
            (
                item
                for item in metadata
                if isinstance(item, (list, tuple)) and item
            ),
            None,
        )
        arguments.append(
            ParserArgument(
                name=parameter.name,
                argument_type=argument_type,
                description=description,
                choices=choices,
                default=parameter.default,
            )
        )

    PARSERS[command_name] = ParserCommandSpec(function, tuple(arguments))
    return function


def create_query() -> argparse.ArgumentParser:
    """Build the root argument parser from all registered commands."""
    parser = argparse.ArgumentParser(prog="bank", description="Bank Management System")
    commands = parser.add_subparsers(dest="command", required=True)

    for command_name, command in PARSERS.items():
        command_parser = commands.add_parser(
            command_name,
            description=inspect.getdoc(command.function),
        )

        for argument in command.arguments:
            options: dict[str, Any] = {"type": argument.argument_type}
            if argument.description is not None:
                options["help"] = argument.description
            if argument.choices is not None:
                options["choices"] = argument.choices
            if argument.default is not inspect.Parameter.empty:
                options["default"] = argument.default
                options["nargs"] = "?"

            command_parser.add_argument(argument.name, **options)

        command_parser.set_defaults(handler=command.function)

    return parser
