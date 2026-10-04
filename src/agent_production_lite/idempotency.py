from hashlib import sha256

from .models import TaskRequest


def build_resource_idempotency_key(request: TaskRequest, resource_id: str | None) -> str | None:
    """Key replay protection to the resource/action/version, not only the task id."""
    if not resource_id:
        return None

    payload = f"{resource_id}:{request.action}:{request.operation_version}".encode("utf-8")
    return sha256(payload).hexdigest()
