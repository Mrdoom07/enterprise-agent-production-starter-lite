from .models import AgentState, Decision, IndependentValidation, RiskLevel, Status, TaskRequest


def decide(
    request: TaskRequest,
    state: AgentState,
    validation: IndependentValidation,
    threshold: float = 0.80,
    idempotency_key: str | None = None,
) -> Decision:
    if state.status == Status.FAILED:
        route, reason = "HUMAN_REVIEW", "worker_error"
    elif request.risk_level == RiskLevel.HIGH:
        route, reason = "HUMAN_APPROVAL", "high_risk_action"
    elif validation.score < threshold:
        route, reason = "HUMAN_REVIEW", "independent_validation_failed"
    elif request.requires_evidence and not state.evidence:
        route, reason = "REWORK", "missing_evidence"
    else:
        route, reason = "ALLOW", "policy_checks_passed"

    return Decision(
        task_id=request.task_id,
        route=route,
        reason=reason,
        state=state,
        validation=validation,
        idempotency_key=idempotency_key,
    )
