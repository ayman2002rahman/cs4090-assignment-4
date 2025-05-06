import pytest
from tasks import filter_tasks_by_priority, search_tasks

@pytest.fixture
def tasks():
    return [
        {"id": 1, "title": "Alpha",   "description": "", "priority": "High", "category": "X", "completed": False},
        {"id": 2, "title": "Beta",    "description": "", "priority": "Medium", "category": "Y", "completed": True},
        {"id": 3, "title": "Gamma",   "description": "", "priority": "Low", "category": "X", "completed": False},
    ]

@pytest.mark.parametrize("prio,expected", [
    ("High",   [1]),
    ("Medium", [2]),
    ("Low",    [3]),
    ("None",   []),
])
def test_filter_priority_param(tasks, prio, expected):
    out = filter_tasks_by_priority(tasks, prio)
    assert [t["id"] for t in out] == expected

@pytest.mark.parametrize("query,expected", [
    ("alpha", [1]),
    ("GAM",   [3]),
    ("z",     []),
])
def test_search_tasks_param(tasks, query, expected):
    out = search_tasks(tasks, query)
    assert [t["id"] for t in out] == expected
