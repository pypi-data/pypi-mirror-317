# Getting started with the jupyter client!
# We would eventually like to make a neovim plugin that can be used to work with jupyter notebooks.

from typing import Annotated
import typer
import uvloop
import shutil
import subprocess
import tempfile

from jupyter_client import AsyncKernelManager, kernelspecapp
from rich import print as rprint

from .schema import Message

app = typer.Typer(name="JupyterClientLearning")


async def amain(kernel_name: str, list_kernels: bool):
    """Start playing around with the jupyter client."""
    specs_manager = kernelspecapp.KernelSpecManager()
    all_specs = specs_manager.get_all_specs()
    kernel_names = [k for k in all_specs.keys()]

    if list_kernels:
        rprint(kernel_names)

    if kernel_name not in kernel_names:
        print("[ERROR] Kernel '{}' not an installed jupyter kernel".format(kernel_name))
        print("[ERROR] Available kernels:")
        print(kernel_names)
    else:
        print(
            "[STARTUP] Starting new jupyter client for kernel: '{}'".format(
                kernel_name)
        )

    akm = AsyncKernelManager(kernel_name=kernel_name)
    await akm.start_kernel()

    kernel_client = akm.client()
    # rprint(kernel_client)
    # print(kernel_client.get_connection_info())

    while True:
        try:
            inp = input("--- ")
            msg_id = kernel_client.execute(inp)
            # print(f"Kernel replied: {reply}")
            # rprint(msg_id)

            # Now consume messages
            executing = True
            while executing:
                msg = Message(**await kernel_client.get_iopub_msg(timeout=1.0))
                # rprint(msg)
                # if msg["parent_header"]["msg_id"] == msg_id:
                # rprint(msg.content)
                # rprint(f"Message type: '{msg.header.msg_type}'")
                try:
                    if "data" in msg.content:
                        data = msg.content["data"]
                        if "text/plain" in data:
                            print("Execution result: {}".format(
                                data["text/plain"]))
                        if "image/png" in data:
                            print("Received png image data!!")
                            # print(data["image/png"])
                            viu_executable = shutil.which("viu")

                            # Write png file to temporary content
                            # cmds = [viu_executable, "-"]
                            # out = subprocess.run(cmds, input=data["image/png"].encode())
                            # print(cmds)
                            # print(out)

                            with tempfile.NamedTemporaryFile(
                                suffix=".png", delete=False
                            ) as temp_file:
                                import base64

                                temp_file_path = temp_file.name
                                png_bytes = base64.decodebytes(
                                    data["image/png"].encode()
                                )
                                temp_file.write(png_bytes)

                            # Use the viu tool to display the image
                            try:
                                subprocess.run(
                                    ["viu", temp_file_path], check=True)
                            finally:
                                pass
                                # Optionally clean up the temporary file
                                import os

                                os.remove(temp_file_path)
                                # print(msg.content["data"])

                    if msg.content["execution_state"] == "idle":
                        # rprint("------ All done ---------")
                        executing = False
                except KeyError:
                    pass
                    # print("Still executing..")

            # msg = await kernel_client.get_iopub_msg()
            # rprint(msg)

            # something_else = await kernel_client.get_shell_msg()
            # rprint(something_else)

        except EOFError:
            print("Requesting shutdown.")
            await akm.request_shutdown()
            print("Sent request!")
            await akm.finish_shutdown()
            print("Request complete! BYE BYE")
            break


@app.command()
def main(
    kernel_name: Annotated[str, typer.Argument] = "python3",
    list_kernels: Annotated[bool, typer.Option] = True,
):
    # Create a new kernel manager
    uvloop.run(amain(kernel_name, list_kernels))


if __name__ == "__main__":
    app()
