"""FastAPI webserver to interact with different jupyter kernels."""

import os
import tempfile
import time
from typing import Annotated

import typer
from fastapi import Depends, FastAPI, HTTPException, status
from jupyter_client import AsyncKernelManager, kernelspecapp

from ..schema import Message
from . import schema
from .dependencies import get_application_state
from .lifespan import lifespan
from .logger import logger
from .state import ApplicationState

app = FastAPI(lifespan=lifespan, title="JupyterKernelServer")


def list_available_kernels() -> list[str]:
    """Retrieve a list of kernel names supported by this machine/environmen."""
    specs_manager = kernelspecapp.KernelSpecManager()
    all_specs = specs_manager.get_all_specs()
    return [k for k in all_specs.keys()]


@app.get("/")
def read_root():
    """Heartbeat for the kernel manager webserver."""
    return {"Hello": "Kernel"}


# ============
# Kernel spec
# ============
@app.get("/kernelspec/list")
def read_kernelspec_list() -> list[str]:
    """Retrieve a list of jupyter kernels supported in by this machine/environment."""
    kernel_names = list_available_kernels()
    return kernel_names


# ============
# Kernels
# ============
@app.get("/kernel/list")
def read_kernel_list(
    app_state: Annotated[ApplicationState, Depends(get_application_state)],
) -> list[str]:
    """Retrieve a list of currently running kernels."""
    return list(app_state.kernel_clients.keys())


@app.get("/kernel/clients")
async def read_kernel_clients(
    app_state: Annotated[ApplicationState, Depends(get_application_state)],
) -> dict:
    """Retrieve information about currently running clients."""
    return {
        kernel_name: (await client.kernel_info(reply=True))["content"]
        for kernel_name, client in app_state.kernel_clients.items()
    }


@app.post("/kernel/start")
async def post_kernel_start(
    kernel: schema.Kernel,
    app_state: Annotated[ApplicationState, Depends(get_application_state)],
) -> dict:
    """Try and start a new kernel managed by this jupyter server."""
    if kernel.name in app_state.kernel_clients:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kernel: '{}' is already running.".format(kernel.name),
        )

    if kernel.name not in list_available_kernels():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kernel: '{}' not available on this machine.".format(kernel.name),
        )

    # Otherwise let's boot up the requested kernel
    akm = AsyncKernelManager(kernel_name=kernel.name)
    tic = time.time()
    await akm.start_kernel()
    kernel_client = akm.client()
    logger.info("Requested Kernel Startup for kernel: {}".format(kernel.name))
    app_state.kernel_clients[kernel.name] = kernel_client
    app_state.kernel_managers[kernel.name] = akm

    # Wait for kernel info as a blocking startup check
    await kernel_client.kernel_info(reply=True)
    toc = time.time()
    logger.info("Kernel startup complete. (elapsed time: {:03}s)".format(toc - tic))

    # Now send a bullshit ping message because otherwise something goes wrong
    # try:
    #     msg_id = kernel_client.execute("")
    #     await kernel_client.get_iopub_msg(timeout=0.01)
    # except Exception:
    #     print(
    #         "Empty ping message sent, no response received (as expected): <id: {}>".format(
    #             msg_id
    #         )
    #     )

    return dict(status="Kernel: '{}' started".format(kernel.name))


@app.post("/kernel/execute")
async def post_kernel_execute(
    payload: schema.ExecutionRequest,
    app_state: Annotated[ApplicationState, Depends(get_application_state)],
) -> dict:
    """Try and execute a piece of code in a given kernel.

    Parameters
    ----------
    payload : schema.ExecutionRequest
        A payload containing the kernel name and source code to execute

    app_state : Annotated[ApplicationState, Depends(get_application_state)]
        application state that will be internally updated

    Returns
    -------
    dict The content response from the kernel
    """
    if payload.kernel_name not in app_state.kernel_clients:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kernel: '{}' not currently running.".format(payload.kernel_name),
        )

    # Otherwise let's grab the appropriate kernel and try and execute some code.
    kernel_client = app_state.kernel_clients[payload.kernel_name]
    logger.info(
        "[{kernel_name}] Executing: '{source_code}'".format(
            kernel_name=payload.kernel_name,
            source_code=payload.source_code,
        )
    )
    logger.info("Is kernel alive? {}".format(await kernel_client.is_alive()))
    msg_id = kernel_client.execute(payload.source_code + "\n")
    logger.info("Sent message with id: {}".format(msg_id))

    # Consume Messages while the kernel is executing code
    executing = True
    while executing:
        logger.info("Waiting for kernel client to receive iopub msg...")
        try:
            msg = Message(**await kernel_client.get_iopub_msg(timeout=1.0))
        except Exception:
            logger.info("No iopub_msg received.")

            try:
                kernel_logs = await kernel_client.get_shell_msg(timeout=1)
                logger.info("Kernel Logs: '{}'".format(kernel_logs))
                return dict(logs=kernel_logs)

            except Exception:
                logger.info("No shell message either!!!")
                return dict(status="Ay carumba")

        # rprint(msg)
        # if msg["parent_header"]["msg_id"] == msg_id:
        # rprint(msg.content)
        # rprint(f"Message type: '{msg.header.msg_type}'")
        if "data" in msg.content:
            data = msg.content["data"]
            logger.info(f"Data: {data}")
        #     if "text/plain" in data:
        #         print("Execution result: {}".format(data["text/plain"]))
        #     if "image/png" in data:
        #         print("Received png image data!!")
        #         # print(data["image/png"])
        #         viu_executable = shutil.which("viu")
        #
        #         # Write png file to temporary content
        #         # cmds = [viu_executable, "-"]
        #         # out = subprocess.run(cmds, input=data["image/png"].encode())
        #         # print(cmds)
        #         # print(out)
        #
        #         with tempfile.NamedTemporaryFile(
        #             suffix=".png", delete=False
        #         ) as temp_file:
        #             import base64
        #
        #             temp_file_path = temp_file.name
        #             png_bytes = base64.decodebytes(data["image/png"].encode())
        #             temp_file.write(png_bytes)
        #
        #         # Use the viu tool to display the image
        #         try:
        #             subprocess.run(["viu", temp_file_path], check=True)
        #         finally:
        #             pass
        #             # Optionally clean up the temporary file
        #             import os
        #
        #             os.remove(temp_file_path)
        #             # print(msg.content["data"])
        #
        if (
            "execution_state" in msg.content
            and msg.content["execution_state"] == "idle"
        ):
            executing = False
            return data

    return dict(status="Loop Exited, but what the fuck?")


# Add typer CLI to actually run the script
cli = typer.Typer(
    name="jupyter_http_client",
    no_args_is_help=True,
)

TEMP_SUBDIR = "jupyter_http_manager"


@cli.command()
def main(host: str = "127.0.0.1", port: int = None):
    """Run a HTTP-server to manage different jupyter kernels."""
    import socket

    import uvicorn

    if port is None:

        def find_free_port():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("localhost", 0))  # 0 means "pick an available port"
            port = s.getsockname()[1]
            s.close()
            return port

        port = find_free_port()

    # We are going to write to a standard temp file the number of the port that we want to use
    temp_base_dir = tempfile.gettempdir()
    temp_dir = os.path.join(temp_base_dir, TEMP_SUBDIR)
    os.makedirs(temp_dir, exist_ok=True)

    logger.info(
        "Starting HTTP-server on host: {host}:{port}".format(host=host, port=port)
    )
    out_dict = dict(port=port, host=host)
    print(out_dict)
    uvicorn.run(app, host=host, port=port)
