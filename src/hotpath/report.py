from pathlib import Path

from hotpath.models import Finding

SEVERITY_ORDER = {"info": 0, "warning": 1, "error": 2}


def render_findings(
    path: Path,
    findings: list[Finding],
    min_severity: str = "info",
) -> str:
    threshold = SEVERITY_ORDER[min_severity]
    visible = [f for f in findings if SEVERITY_ORDER[f.severity] >= threshold]

    lines = [f"HotPath analysis: {path}", ""]
    if not visible:
        lines.append("No findings at the selected severity.")
        return "\n".join(lines)

    for index, finding in enumerate(visible, start=1):
        lines.append(
            f"{index}. [{finding.severity.upper()}] {finding.title} "
            f"({finding.rule_id})"
        )
        lines.append(f"   Line {finding.line}: {finding.message}")
        lines.append(f"   Fix: {finding.recommendation}")
        if finding.example:
            lines.append("   Example:")
            for example_line in finding.example.splitlines():
                lines.append(f"     {example_line}")
        lines.append("")

    return "\n".join(lines).rstrip()


def render_project_findings(
    results: dict[Path, list[Finding]],
    min_severity: str = "info",
) -> str:
    threshold = SEVERITY_ORDER[min_severity]
    files_with_visible = {
        path: [f for f in findings if SEVERITY_ORDER[f.severity] >= threshold]
        for path, findings in results.items()
    }
    files_with_visible = {
        path: findings for path, findings in files_with_visible.items() if findings
    }

    total = sum(len(findings) for findings in files_with_visible.values())
    lines = [f"HotPath project analysis: {total} findings across {len(files_with_visible)} files", ""]
    if not files_with_visible:
        lines.append("No findings at the selected severity.")
        return "\n".join(lines)

    for path, findings in sorted(files_with_visible.items()):
        lines.append(str(path))
        for finding in findings:
            lines.append(
                f"  [{finding.severity.upper()}] {finding.rule_id} line {finding.line}: "
                f"{finding.title}"
            )
            lines.append(f"    {finding.recommendation}")
        lines.append("")
    return "\n".join(lines).rstrip()
