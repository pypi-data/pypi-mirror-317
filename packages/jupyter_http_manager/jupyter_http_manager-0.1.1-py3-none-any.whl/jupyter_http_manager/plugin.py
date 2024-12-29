"""Pynvim powered plugin to process jupyter notebooks."""

from datetime import datetime
from typing import Annotated

import nbformat
import orjson
import pynvim
import typer
from rich import print as rprint

app = typer.Typer(name="LuaNotebooks")


def wrap_string(string: str, wrapper: str = "'") -> str:
    """Add a prefix and postfix to a string.

    Arguments
    ---------
    string : str

    wrapper : str


    Returns
    -------
    str
        The input string wrapped with the `wrapper`.
    """
    return wrapper + string + wrapper


def list_to_lua_table(lines: list[str]) -> str:
    """Convert a list of strings into a lua table.

    Arguments
    ---------
    lines : list[str]


    Returns
    -------
    str
       Lua code representation of a table

    Examples
    --------
    ```
    >>> list_to_lua_table(['hi', 'howdy'])
    "{'hi', 'howdy'}"
    ```
    """
    start = "{"
    end = "}"
    s = ""
    for line in lines[:-1]:
        s += wrap_string(line) + ", "
    s += wrap_string(lines[-1])
    return start + s + end


def append_lines_lua(bufnr: int, lines: list[str]) -> str:
    """Generate Lua code that will append lines to an nvim buffer.

    Parameters
    ----------
    bufnr : int
        The unique identifier of the buffer inside of lua

    lines : list[str]
        The lines we would like to append to our buffer

    Returns
    -------
    str
        Lua code that can be executed inside of an nvim context.
    """
    lua_code = """local line_count = vim.api.nvim_buf_line_count({bufnr})
vim.api.nvim_buf_set_lines({bufnr}, line_count, line_count, false, {lines})""".format(
        bufnr=bufnr, lines=list_to_lua_table(lines)
    )

    return lua_code


@app.command()
def main(
    server_file: Annotated[
        str,
        typer.Argument(
            help="The server file that an instance of nvim is currently running. Run `echo v:servername` to get this output"
        ),
    ],
    jupyter_notebook_bufnr: Annotated[
        int,
        typer.Argument(
            help="The bufnr of a _popup_ buffer that will be used to interact with our jupyter notebook."
        ),
    ],
    jupyter_notebook_file: Annotated[
        str,
        typer.Argument(
            help="The full path to a jupyter notebook that we would like to work with."
        ),
    ],
):
    """Start a python neovim plugin connects to a running instance of nvim."""
    rprint("Hello Notebooks.")
    rprint("Running on server_file: {}".format(server_file))
    rprint("Using jupyter buffer number: {}".format(jupyter_notebook_bufnr))
    rprint("Loading jupyter file: {}".format(jupyter_notebook_file))

    nvim = pynvim.attach("socket", path=server_file)
    rprint(nvim)
    nvim.exec_lua(
        append_lines_lua(
            jupyter_notebook_bufnr, ["Executed on: " + str(datetime.now())]
        )
    )

    with open(jupyter_notebook_file) as jupyter_file:
        content = jupyter_file.readlines()
        single_string = "".join(content)
        # rprint(single_string)
        notebook_dict = orjson.loads(single_string)
        rprint("Using notebook version: {}".format(notebook_dict["nbformat"]))

        # My actual notebook object
        notebook = nbformat.from_dict(notebook_dict)

        rprint(type(notebook))
        rprint("Number cells: {}".format(len(notebook.cells)))

        from nbformat.v4 import new_markdown_cell

        md_cell = new_markdown_cell("# My header")

        notebook.cells.append(md_cell)
        rprint("Number cells: {}".format(len(notebook.cells)))

        # Now let's actually start displaying those cells inside of nvim!
        for cell in notebook.cells:
            # rprint("Cell type: {}".format(cell.cell_type))
            display_string = "[{cell_type}][{cell_type}]".format(
                cell_type=cell.cell_type
            )

            if cell.cell_type == "code":
                display_string = "```\n{}```".format("".join(cell.source))
            else:
                display_string = cell.source

            print(display_string)

        # rprint(md_cell)

        # rprint(notebook.cells)

    # Try and load in the notebook file as a string

    # Let's try and add some content to this buffer letting us visualize that we are
    # indeed interacting with the server
    # nvim.exec_lua(
    #     """
    #     vim.api.nvim
    #     """,
    #     async_=True,
    # )
