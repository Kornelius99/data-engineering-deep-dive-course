from datetime import datetime, timedelta, timezone

from checks import (
    check_completeness,
    check_freshness,
    check_referential_integrity,
    check_row_count_anomaly,
    check_uniqueness,
)


def test_completeness_passes_when_no_nulls():
    rows = [{"a": 1}, {"a": 2}, {"a": 3}]
    result = check_completeness(rows, "a")
    assert result.passed


def test_completeness_fails_when_too_many_nulls():
    rows = [{"a": 1}, {"a": None}, {"a": None}]
    result = check_completeness(rows, "a", max_null_fraction=0.1)
    assert not result.passed


def test_uniqueness_detects_duplicates():
    rows = [{"id": 1}, {"id": 2}, {"id": 1}]
    result = check_uniqueness(rows, ["id"])
    assert not result.passed


def test_uniqueness_passes_when_unique():
    rows = [{"id": 1}, {"id": 2}, {"id": 3}]
    result = check_uniqueness(rows, ["id"])
    assert result.passed


def test_referential_integrity_detects_orphans():
    child_rows = [{"city_id": 1}, {"city_id": 99}]
    result = check_referential_integrity(child_rows, "city_id", parent_ids=[1, 2])
    assert not result.passed


def test_freshness_passes_when_recent():
    now = datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc)
    rows = [{"observed_at": now - timedelta(hours=2)}]
    result = check_freshness(rows, "observed_at", now, max_age_hours=26)
    assert result.passed


def test_freshness_fails_when_stale():
    now = datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc)
    rows = [{"observed_at": now - timedelta(hours=48)}]
    result = check_freshness(rows, "observed_at", now, max_age_hours=26)
    assert not result.passed


def test_row_count_anomaly_flags_spike():
    result = check_row_count_anomaly(today_count=500, historical_counts=[24, 25, 23, 24, 26])
    assert not result.passed


def test_row_count_anomaly_passes_normal_count():
    result = check_row_count_anomaly(today_count=25, historical_counts=[24, 25, 23, 24, 26])
    assert result.passed
