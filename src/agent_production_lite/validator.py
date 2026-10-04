import re

from .models import IndependentValidation, Status, TaskRequest


def validate_independently(request: TaskRequest, worker_status: Status) -> IndependentValidation:
    """Validate request context without trusting model/worker self-confidence.

    The parser reads the original request text directly. In a production system this
    layer would be fed authoritative, normalized tool data rather than model-authored
    summaries.
    """
    raw = request.input_data.strip()
    references = re.findall(r"\b\d{3,}\b", raw)
    resolved_resource_id = request.resource_id or (references[0] if references else None)

    reasons: list[str] = []
    if worker_status != Status.COMPLETE:
        reasons.append("worker_not_complete")
    if not resolved_resource_id:
        reasons.append("resource_not_resolved")

    if worker_status != Status.COMPLETE:
        score = 0.0
    elif resolved_resource_id:
        score = 1.0
    else:
        score = 0.55

    return IndependentValidation(
        score=score,
        resource_resolved=resolved_resource_id is not None,
        resolved_resource_id=resolved_resource_id,
        reasons=reasons,
    )
