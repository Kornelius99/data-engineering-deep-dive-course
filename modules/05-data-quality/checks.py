"""Module 05: five data quality checks that operate on plain Python lists of
dicts, so they're unit-testable without a live database (see tests/).

In a real pipeline you'd run these against query results from your
warehouse - the logic is identical either way.
"""
from dataclasses import dataclass, field
from statistics import mean, pstdev
from typing import Any, Dict, List, Optional


@dataclass
class CheckResult:
    name: str
    passed: bool
    details: str


def check_completeness(rows: List[Dict[str, Any]], field_name: str, max_null_fraction: float = 0.01) -> CheckResult:
    if not rows:
        return CheckResult("completeness", False, "no rows to check")
    nulls = sum(1 for r in rows if r.get(field_name) is None)
    fraction = nulls / len(rows)
    passed = fraction <= max_null_fraction
    return CheckResult(
        "completeness",
        passed,
        f"{field_name}: {nulls}/{len(rows)} null ({fraction:.2%}), threshold {max_null_fraction:.2%}",
    )


def check_uniqueness(rows: List[Dict[str, Any]], key_fields: List[str]) -> CheckResult:
    seen = set()
    duplicates = 0
    for r in rows:
        key = tuple(r.get(k) for k in key_fields)
        if key in seen:
            duplicates += 1
        seen.add(key)
    passed = duplicates == 0
    return CheckResult("uniqueness", passed, f"{duplicates} duplicate key(s) on {key_fields}")


def check_referential_integrity(
    child_rows: List[Dict[str, Any]], child_key: str, parent_ids: List[Any]
) -> CheckResult:
    parent_set = set(parent_ids)
    orphans = [r for r in child_rows if r.get(child_key) not in parent_set]
    passed = len(orphans) == 0
    return CheckResult("referential_integrity", passed, f"{len(orphans)} orphaned row(s) on {child_key}")


def check_freshness(rows: List[Dict[str, Any]], timestamp_field: str, now, max_age_hours: float = 26) -> CheckResult:
    if not rows:
        return CheckResult("freshness", False, "no rows to check")
    latest = max(r[timestamp_field] for r in rows if r.get(timestamp_field) is not None)
    age_hours = (now - latest).total_seconds() / 3600
    passed = age_hours <= max_age_hours
    return CheckResult("freshness", passed, f"latest row is {age_hours:.1f}h old, threshold {max_age_hours}h")


def check_row_count_anomaly(
    today_count: int, historical_counts: List[int], z_threshold: float = 2.0
) -> CheckResult:
    if len(historical_counts) < 3:
        return CheckResult("row_count_anomaly", True, "not enough history to evaluate, skipping")
    mu = mean(historical_counts)
    sigma = pstdev(historical_counts) or 1e-9
    z = (today_count - mu) / sigma
    passed = abs(z) <= z_threshold
    return CheckResult("row_count_anomaly", passed, f"today={today_count}, mean={mu:.1f}, z={z:.2f}")


def check_all(results: List[CheckResult]) -> bool:
    return all(r.passed for r in results)
