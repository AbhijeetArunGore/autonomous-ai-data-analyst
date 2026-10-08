import pytest
from evaluations.benchmark_runner import BenchmarkRunner

def test_benchmark_suite_execution():
    report = BenchmarkRunner.run_all_benchmarks("datasets/benchmarks")
    assert report.total_benchmarks_run >= 3
    assert report.overall_pass_rate == 100.0
    assert len(report.results) >= 3
    for res in report.results:
        assert res.numerical_correctness_pct == 100.0
        assert res.validation_passed is True
