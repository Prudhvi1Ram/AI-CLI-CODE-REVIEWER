import json 
from pathlib import Path


def generate_json_report(report,outputh_path):
    outputh_path=Path(outputh_path)
    with outputh_path.open("w",encoding="utf-8") as file:
        json.dump(
            report.model_dump(mode="json"),
            file,
            indent=4
        )
def generate_markdown_report(report, output_path):
    output_path = Path(output_path)

    lines = [
        f"# Code Review Report: {report.file_name}",
        "",
        f"**Overall Status:** {report.overall_status}",
        "",
        "## Summary",
        "",
        report.summary,
        "",
        "## Findings",
        ""
    ]

    if not report.findings:
        lines.append("No issues found.")
    else:
        for index, finding in enumerate(report.findings, start=1):

            severity = getattr(finding.severity, "value", finding.severity)

            lines.extend([
                f"### {index}. {finding.category}",
                "",
                f"- **Severity:** {severity}",
                f"- **Line:** {finding.line}",
                "",
                "**Issues:**",
                ""
            ])

            for issue in finding.issues:
                lines.append(f"- {issue}")

            lines.extend([
                "",
                "**Suggestion:**",
                "",
                finding.suggestion,
                "",
                "---",
                ""
            ])

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )
    

    
