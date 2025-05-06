import json
import os
from datetime import datetime, timedelta
import pytest

from tasks import (
    load_tasks,
    save_tasks,
    generate_unique_id,
    filter_tasks_by_priority,
    filter_tasks_by_category,
    filter_tasks_by_completion,
    search_tasks,
    get_overdue_tasks,
)

def test_load_tasks_nonexistent(tmp_path):
    path = tmp_path / "no_exist.json"
    # should return empty list, not raise
    assert load_tasks(str(path)) == []

def test_load_tasks_corrupted(tmp_path, capsys):
    # write invalid JSON
    path = tmp_path / "bad.json"
    path.write_text("{ invalid json }")
    tasks = load_tasks(str(path))
    captured = capsys.readouterr()
    assert "contains invalid JSON" in captured.out
    assert tasks == []

def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "tasks.json"
    sample = [{"id": 1, "title": "X"}]
    save_tasks(sample, str(path))
    loaded = load_tasks(str(path))
    assert loaded == sample

def test_generate_unique_id_empty():
    assert generate_unique_id([]) == 1

def test_generate_unique_id_nonempty():
    tasks = [{"id": 1}, {"id": 4}, {"id": 2}]
    assert generate_unique_id(tasks) == 5

@pytest.fixture
def sample_tasks():
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    return [
        {"id": 1, "title": "A", "description": "foo", "priority": "High",
         "category": "Work",  "completed": False, "due_date": yesterday},
        {"id": 2, "title": "B", "description": "bar", "priority": "Low",
         "category": "Home",  "completed": True,  "due_date": today},
    ]

def test_filter_by_priority(sample_tasks):
    out = filter_tasks_by_priority(sample_tasks, "High")
    assert [t["id"] for t in out] == [1]

def test_filter_by_category(sample_tasks):
    out = filter_tasks_by_category(sample_tasks, "Home")
    assert [t["id"] for t in out] == [2]

def test_filter_by_completion(sample_tasks):
    out = filter_tasks_by_completion(sample_tasks, completed=False)
    assert [t["id"] for t in out] == [1]

def test_search_tasks_matches_title_and_description(sample_tasks):
    by_title = search_tasks(sample_tasks, "A")
    by_desc  = search_tasks(sample_tasks, "bar")
    assert [t["id"] for t in by_title] == [1]
    assert [t["id"] for t in by_desc]  == [2]

def test_get_overdue_tasks(sample_tasks):
    # only task 1 is overdue and incomplete
    overdue = get_overdue_tasks(sample_tasks)
    assert [t["id"] for t in overdue] == [1]
