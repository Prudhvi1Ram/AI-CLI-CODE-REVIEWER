import os,json
from dotenv import load_dotenv
from groq import Groq
from reviewer.schemas import CodeReviewReport
load_dotenv()
client=Groq(
    api_key=os.environ["GROQ_API_KEY"]
)



def code_report(code, ruff_findings, ast_findings,file_name):

    chat = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "system",
                "content": """
                You are an expert Python code reviewer.

                Analyze the provided code for:
                - Logical bugs
                - Security vulnerabilities
                - Performance issues
                - Code quality problems

                Return a JSON object containing:
                overall_status, summary, and findings.

                Every finding must contain issue_type, category, severity, line, issues, and suggestion.

                Return valid JSON only.
                IMPORTANT:
                - The "issues" field must ALWAYS be a list of strings.
                - Even if there is only one issue, return it as a list containing one string.
                - Never return "issues" as a single string.
                You MUST return a valid JSON object.

Follow this exact structure:

{
    "overall_status": "Critical",
    "summary": "Explanation of the overall code quality.",
    "findings": [
        {
    "issue_type": "sql_injection",
    "category": "Security",
    "severity": "High",
    "line": 7,
    "issues": [
        "Description of the issue."
    ],
    "suggestion": "How to fix the issue."
}
    ]
}
For every finding, include an issue_type field.

Use one of these standardized labels:
- logical_bug
- undefined_variable
- inefficient_loop
- sql_injection
- infinite_loop
- resource_leak
- bare_except
- mutable_default_argument
- other

Always use the closest matching label. If none applies, use "other".

STRICT RULES:
1. Return JSON only. No Markdown or code fences.
2. Every finding must contain category, severity, line, issues, and suggestion.
3. The issues field MUST always be a list of strings.
4. Never return issues as a single string.
5. Do not add fields that are not part of the specified structure.
6. Do not include file_name. The application adds it separately.
7. Ensure all JSON strings are properly escaped.
                """
            },
            {
                "role": "user",
                "content": f"""
                Python code:
                {code}

                Ruff findings:
                {ruff_findings}

                AST findings:
                {ast_findings}
                """
            }
        ],
        response_format={
        "type": "json_object"
}
    )

    response = chat.choices[0].message.content
    report_data=json.loads(response)
    report_data["file_name"]=file_name
    for finding in report_data["findings"]:
        if isinstance(finding["issues"], str):
            finding["issues"] = [finding["issues"]]

    report = CodeReviewReport.model_validate(report_data)

    return report




