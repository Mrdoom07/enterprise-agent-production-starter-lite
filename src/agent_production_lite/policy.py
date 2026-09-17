from .models import AgentState, Decision, RiskLevel, Status, TaskRequest


def decide(request: TaskRequest, state: AgentState, threshold: float = 0.80) -> Decision:
    """Keep policy outside the worker/model boundary."""
    if state.status == Status.FAILED:
        route, reason = "HUMAN_REVIEW", "worker_error"
    elif request.risk_level == RiskLevel.HIGH:
        route, reason = "HUMAN_APPROVAL", "high_risk_action"
    elif state.confidence_score < threshold:
        route, reason = "HUMAN_REVIEW", "low_confidence"
    elif request.requires_evidence and not state.evidence:
        route, reason = "REWORK", "missing_evidence"
    else:
        route, reason = "ALLOW", "policy_checks_passed"

    return Decision(
        task_id=request.task_id,
        route=route,
        reason=reason,
        state=state,
    )
