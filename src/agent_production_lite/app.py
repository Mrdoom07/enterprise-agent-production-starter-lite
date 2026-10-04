from fastapi import FastAPI

from .audit import list_records
from .models import Decision, TaskRequest
from .service import validate_task

app = FastAPI(
    title="Enterprise AI Agent Production Starter — Lite",
    version="0.2.0",
    description="Reference boundary for typed agent state, independent validation, policy routing, idempotency and audit logging. No external side effects are performed.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/tasks/validate", response_model=Decision)
def validate(request: TaskRequest) -> Decision:
    return validate_task(request)


@app.get("/v1/audit")
def audit_log() -> list[dict[str, str | None]]:
    return list_records()
