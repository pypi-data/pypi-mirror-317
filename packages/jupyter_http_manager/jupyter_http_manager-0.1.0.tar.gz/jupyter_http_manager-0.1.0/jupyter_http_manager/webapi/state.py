"""Global Application State."""

from dataclasses import dataclass, field
from jupyter_client import AsyncKernelClient, AsyncKernelManager
from collections import OrderedDict


# TODO: We need to implement a better data structure for the actual kernels that are active
@dataclass
class ApplicationState:
    """Top-level class encapsulating global state for an application."""

    kernel_clients: OrderedDict[str, AsyncKernelClient] = field(
        default_factory=OrderedDict
    )
    kernel_managers: OrderedDict[str, AsyncKernelManager] = field(
        default_factory=OrderedDict
    )

    async def shutdown_kernels(self):
        """Request shutdown of all running kernels."""
        for kernel_name, akm in self.kernel_managers.items():
            print("Requesting shutdown for kernel: {}".format(kernel_name))
            await akm.request_shutdown()
            await akm.finish_shutdown()
