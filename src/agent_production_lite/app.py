from fastapi import FastAPI

from .models import Decision, TaskRequest
from .service import validate_task

app = FastAPI(
    title="Enterprise AI Agent Production Starter — Lite",
    version="0.1.0",
    description="Reference boundary for typed agent state, policy routing and human escalation. No external side effects are performed.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/tasks/validate", response_model=Decision)
def validate(request: TaskRequest) -> Decision:
    return validate_task(request)
