from .models import Decision, TaskRequest
from .policy import decide
from .worker import demo_worker


def validate_task(request: TaskRequest) -> Decision:
    state = demo_worker(request.input_data)
    return decide(request, state)
