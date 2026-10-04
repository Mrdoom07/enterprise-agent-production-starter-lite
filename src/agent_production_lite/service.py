from .audit import record_decision
from .idempotency import build_resource_idempotency_key
from .models import Decision, TaskRequest
from .policy import decide
from .validator import validate_independently
from .worker import demo_worker


def validate_task(request: TaskRequest) -> Decision:
    state = demo_worker(request.input_data)
    validation = validate_independently(request, state.status)
    idempotency_key = build_resource_idempotency_key(
        request,
        validation.resolved_resource_id,
    )
    decision = decide(
        request,
        state,
        validation,
        idempotency_key=idempotency_key,
    )
    record_decision(decision)
    return decision
