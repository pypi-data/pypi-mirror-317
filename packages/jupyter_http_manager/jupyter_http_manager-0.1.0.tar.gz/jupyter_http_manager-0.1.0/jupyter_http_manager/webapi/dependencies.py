from starlette.requests import Request
from .state import ApplicationState


async def get_application_state(request: Request) -> ApplicationState:
    """Retrieve the application state object.

    `ApplicationState` is initialized in the lifespan function.
    """
    return request.app.state.application_state
