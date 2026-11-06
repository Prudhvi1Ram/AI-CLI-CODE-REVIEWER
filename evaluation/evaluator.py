
import json
from pathlib import Path

from reviewer.static_analyzer import analyze_code
from reviewer.ast_analyzer import analyze_structure
from reviewer.ai_reviewer import code_report

from evaluation.metrics import calculate_metrics


BASE_DIR = Path(__file__).resolve().parent.parent
TEST_DIR = BASE_DIR / "Test-cases"
GROUND_TRUTH_FILE = BASE_DIR / "evaluation" / "actual_output.json"


def run_evaluation():

    with open(GROUND_TRUTH_FILE, "r", encoding="utf-8") as file:
        ground_truth = json.load(file)

    total_tp = 0
    total_fp = 0
    total_fn = 0

    print("\n========== CODE REVIEW EVALUATION ==========\n")

    for file_name, data in ground_truth.items():

        file_path = TEST_DIR / file_name

        if not file_path.exists():
            print(f"Skipping {file_name}: File not found.")
            continue

        # Read Python code
        code = file_path.read_text(encoding="utf-8")

        # Run static analysis
        ruff_findings = analyze_code(str(file_path))

        # Run AST analysis
        ast_findings = analyze_structure(code)

        # Run AI reviewer
        report = code_report(
            code,
            ruff_findings,
            ast_findings,
            file_name
        )

        # Extract expected and predicted issue types
        expected = set(data["expected_findings"])

        predicted = {
            finding.issue_type
            for finding in report.findings
        }

        # Calculate individual test-case metrics
        metrics = calculate_metrics(expected, predicted)

        # Calculate counts for overall evaluation
        tp = len(expected & predicted)
        fp = len(predicted - expected)
        fn = len(expected - predicted) if False else len(expected - predicted)

        # Correct false-negative calculation
        fn = len(expected - predicted)

        total_tp += tp
        total_fp += fp
        total_fn += fn

        print(f"Test case: {file_name}")
        print(f"Expected:  {expected}")
        print(f"Predicted: {predicted}")
        print(f"Precision: {metrics['precision']}")
        print(f"Recall:    {metrics['recall']}")
        print(f"F1-score:  {metrics['f1_score']}")
        print("-" * 45)

    # Calculate overall metrics
    precision = (
        total_tp / (total_tp + total_fp)
        if total_tp + total_fp > 0 else 0.0
    )

    recall = (
        total_tp / (total_tp + total_fn)
        if total_tp + total_fn > 0 else 0.0
    )

    f1_score = (
        2 * precision * recall / (precision + recall)
        if precision + recall > 0 else 0.0
    )

    print("\n========== OVERALL RESULTS ==========")
    print(f"True Positives:  {total_tp}")
    print(f"False Positives: {total_fp}")
    print(f"False Negatives: {total_fn}")
    print(f"Precision:       {precision:.4f}")
    print(f"Recall:          {recall:.4f}")
    print(f"F1-score:        {f1_score:.4f}")


if __name__ == "__main__":
    run_evaluation()
