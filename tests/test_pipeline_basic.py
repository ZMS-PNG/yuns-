from mapes.pipeline import evaluate_file, load_cases


def test_load_demo_cases():
    cases = load_cases("data/cases/demo_cases.json")
    assert len(cases) == 3


def test_evaluate_file_generates_reports(tmp_path):
    output = tmp_path / "report.json"
    reports = evaluate_file("data/cases/demo_cases.json", str(output))
    assert len(reports) == 3
    assert output.exists()
