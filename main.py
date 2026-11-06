import typer
from pathlib import Path
from datetime import datetime
from reviewer.code_reader import read_code
from reviewer.static_analyzer import analyze_code
from reviewer.ast_analyzer import analyze_structure
from reviewer.ai_reviewer import code_report
from reviewer.report_generator import generate_json_report,generate_markdown_report
app = typer.Typer()

@app.command()
def review(file_path: str):
    try:
        code = read_code(file_path)

        print("File loaded successfully!")
        print(f"********* SOURCE CODE *************")
        print(code)
        ruff_findings=analyze_code(file_path)
        print(f"******* CODE ANALYSIS ***********")
        if not ruff_findings:
            print("No issues found!!")
        else:
            for issues in ruff_findings:
                print("Rule:", issues["code"])
                print("Message:", issues["message"])
                print("Line:", issues["location"]["row"])
        ast_structure=analyze_structure(code)
        print(f"******* AST ANALYSIS ********")
        for category,items in ast_structure.items():
            print(f"\n{category.upper()}")
            if not items:
                print("None found")
            else:
                for item in items:
                    print("-",item)
        report=code_report(code,ruff_findings,ast_structure,Path(file_path).name)
        print(f"********* LLM REPORT*********")
        print(report.overall_status)
        print(report.summary)
        print(report.model_dump_json(indent=2))
        timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path=Path("reports") / f"{Path(file_path).stem}_{timestamp}.json"
        generate_json_report(report,report_path)
        generate_markdown_report(report, report_path.with_suffix(".md"))




    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def version():
    print("AI Code Reviewer v1.0")


if __name__ == "__main__":
    app()