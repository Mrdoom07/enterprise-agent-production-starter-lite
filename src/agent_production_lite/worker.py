import re

from .models import AgentState, Status


def demo_worker(text: str) -> AgentState:
    """Deterministic worker used so the repo runs with no model/API key."""
    cleaned = text.strip()
    if not cleaned:
        return AgentState(status=Status.FAILED, confidence_score=0.0)

    invoice_ids = re.findall(r"\b\d{3,}\b", cleaned)
    has_specific_reference = bool(invoice_ids)

    confidence = 0.94 if has_specific_reference else 0.58
    evidence = [f"detected_reference:{invoice_ids[0]}"] if invoice_ids else []

    return AgentState(
        status=Status.COMPLETE,
        confidence_score=confidence,
        evidence=evidence,
        extracted_entities=invoice_ids,
    )
