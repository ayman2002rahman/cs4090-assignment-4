import pytest
from tasks import add_task, generate_unique_id

@pytest.fixture
def empty_list():
    return []

def test_add_task_functionality(empty_list):
    # This will FAIL until you implement add_task()
    task = add_task(empty_list, title="New", priority="Low", due_date="2025-01-01")
    assert "id" in task
    assert task["title"] == "New"
    assert empty_list == [task]
