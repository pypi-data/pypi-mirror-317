from enum import Enum
from pathlib import Path

import typer
from typing_extensions import Annotated

from demilich.reader import (
    generate_skeleton,
    load_from_resources,
    load_from_file,
)
from demilich.output import write_csv, write_table


class OutputFormat(str, Enum):
    csv = "csv"
    table = "table"


app = typer.Typer(no_args_is_help=True)


@app.command()
def play_booster(
    format: Annotated[
        OutputFormat, typer.Option()
    ] = OutputFormat.csv,
    include_instruction: Annotated[
        bool|None, typer.Option(help="Include skeleton instruction")
    ] = None,
    include_text: Annotated[
        bool|None, typer.Option(help="Include card text")
    ] = None,
):
    """
    Generate a standard play booster skeleton.
    """
    data = load_from_resources('pb2024.toml')
    _generate(data, format, include_instruction, include_text)


@app.command()
def custom_skeleton(
    filename: Annotated[
        Path, typer.Argument()
    ],
    format: Annotated[
        OutputFormat, typer.Option()
    ] = OutputFormat.csv,
    include_instruction: Annotated[
        bool|None, typer.Option(help="Include skeleton instruction")
    ] = None,
    include_text: Annotated[
        bool|None, typer.Option(help="Include card text")
    ] = None,
):
    """
    Generate a skeleton from a TOML file.
    """
    data = load_from_file(filename)
    _generate(data, format, include_instruction, include_text)


def _generate(data, format, include_instruction, include_text):
    all_fields = ['id', 'instruction', 'name', 'cost', 'typeline', 'text', 'stats']
    fields = {field: True for field in all_fields}

    if format == OutputFormat.csv:
        fields['instruction'] = False if include_instruction is False else True
        fields['text'] = False if include_text is False else True
        write_csv(generate_skeleton(data), [key for key, value in fields.items() if value])

    elif format == OutputFormat.table:
        fields['instruction'] = True if include_instruction is True else False
        fields['text'] = False if include_text is False else True
        write_table(generate_skeleton(data), [key for key, value in fields.items() if value])

    else:
        raise NotImplementedError(format)


# Left for demonstration purposes - this exercises the example
# in examples/dev.py
# @app.command()
# def dev():
#     """
#     Generate a partial skeleton, exercising a few features.
#     """
#     from demilich.examples.dev import dev_skeleton
#     write_csv(dev_skeleton(), ['id', 'instruction', 'name', 'cost', 'typeline', 'text', 'stats'])
