#!/usr/bin/env python3
"""
Deep Research Skill - Test Runner

Runs validate_report.py against test fixtures to catch regressions.
Does NOT run verify_citations.py (requires network/DOI lookups).

Usage:
    python3 tests/run_tests.py          # Run all tests
    python3 tests/run_tests.py -v       # Verbose output
    python3 tests/run_tests.py --ci     # Exit 1 on any failure (for CI)
"""

import argparse
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
VALIDATE_SCRIPT = SKILL_DIR / "scripts" / "validate_report.py"
FIXTURES_DIR = SKILL_DIR / "tests" / "fixtures"


def test_valid_report(verbose: bool) -> bool:
    """Valid report should PASS all checks (exit 0)."""
    report = FIXTURES_DIR / "valid_report.md"
    if not report.exists():
        print(f"  SKIP: fixture not found: {report}")
        return True

    if verbose:
        print(f"  Running: {VALIDATE_SCRIPT.name} --report {report.name}")
    result = subprocess.run(
        [sys.executable, str(VALIDATE_SCRIPT), "--report", str(report)],
        capture_output=True, text=True
    )

    passed = result.returncode == 0
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  [{status}] valid_report.md (expect PASS)")

    if verbose or not passed:
        _print_output(result)

    return passed


def test_invalid_report(verbose: bool) -> bool:
    """Invalid report should FAIL (exit 1)."""
    report = FIXTURES_DIR / "invalid_report.md"
    if not report.exists():
        print(f"  SKIP: fixture not found: {report}")
        return True

    if verbose:
        print(f"  Running: {VALIDATE_SCRIPT.name} --report {report.name}")
    result = subprocess.run(
        [sys.executable, str(VALIDATE_SCRIPT), "--report", str(report)],
        capture_output=True, text=True
    )

    # Invalid report should fail validation
    passed = result.returncode != 0
    status = "✅ PASS (expected fail)" if passed else "❌ FAIL (unexpected pass)"
    print(f"  [{status}] invalid_report.md (expect FAIL)")

    if verbose or not passed:
        _print_output(result)

    return passed


def test_report_not_found(verbose: bool) -> bool:
    """Non-existent report should exit 1."""
    fake_report = FIXTURES_DIR / "nonexistent.md"
    if verbose:
        print(f"  Running: {VALIDATE_SCRIPT.name} --report nonexistent.md")
    result = subprocess.run(
        [sys.executable, str(VALIDATE_SCRIPT), "--report", str(fake_report)],
        capture_output=True, text=True
    )

    passed = result.returncode != 0
    status = "✅ PASS (expected fail)" if passed else "❌ FAIL"
    print(f"  [{status}] nonexistent report (expect exit 1)")

    if verbose or not passed:
        _print_output(result)

    return passed


def _print_output(result: subprocess.CompletedProcess):
    """Print stdout/stderr from subprocess."""
    out = result.stdout.strip()
    err = result.stderr.strip()
    if out:
        for line in out.split("\n")[:5]:
            print(f"    | {line}")
        if len(out.split("\n")) > 5:
            print(f"    | ... ({len(out.split('\n')) - 5} more lines)")
    if err:
        print(f"    stderr: {err[:200]}")


def main():
    parser = argparse.ArgumentParser(
        description="Run deep-research skill tests against fixtures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 tests/run_tests.py
  python3 tests/run_tests.py -v
  python3 tests/run_tests.py --ci
        """
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--ci", action="store_true", help="CI mode: exit 1 on failure")
    args = parser.parse_args()

    print(f"🔬 Deep Research Skill - Test Runner")
    print(f"   Script: {VALIDATE_SCRIPT.name}")
    print(f"   Fixtures: {FIXTURES_DIR}\n")

    tests = [
        ("Valid report (should pass)", test_valid_report),
        ("Invalid report (should fail)", test_invalid_report),
        ("Non-existent report (should error)", test_report_not_found),
    ]

    passed_count = 0
    failed_count = 0

    for name, test_fn in tests:
        print(f"\n  Test: {name}")
        try:
            ok = test_fn(args.verbose)
            if ok:
                passed_count += 1
            else:
                failed_count += 1
        except Exception as e:
            print(f"  [❌ EXCEPTION] {e}")
            failed_count += 1

    print(f"\n{'=' * 50}")
    print(f"RESULTS: {passed_count}/{len(tests)} passed")
    if failed_count > 0:
        print(f"         {failed_count}/{len(tests)} failed")

    if args.ci and failed_count > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
