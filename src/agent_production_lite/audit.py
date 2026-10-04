from dataclasses import dataclass, asdict
from threading import Lock

from .models import Decision


@dataclass(frozen=True)
class AuditRecord:
    task_id: str
    route: str
    reason: str
    resource_id: str | None
    idempotency_key: str | None


_records: list[AuditRecord] = []
_lock = Lock()


def record_decision(decision: Decision) -> None:
    """Record every policy outcome, including ALLOW decisions.

    This is intentionally in-memory for the Lite demo. Production systems should
    write immutable records to durable storage with timestamps, actor identity,
    evidence references, approval identity, and side-effect status.
    """
    record = AuditRecord(
        task_id=decision.task_id,
        route=decision.route,
        reason=decision.reason,
        resource_id=decision.validation.resolved_resource_id,
        idempotency_key=decision.idempotency_key,
    )
    with _lock:
        _records.append(record)


def list_records() -> list[dict[str, str | None]]:
    with _lock:
        return [asdict(record) for record in _records]


def clear_records() -> None:
    with _lock:
        _records.clear()
