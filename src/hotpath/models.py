from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    rule_id: str
    title: str
    severity: str
    line: int
    message: str
    recommendation: str
    example: str | None = None
