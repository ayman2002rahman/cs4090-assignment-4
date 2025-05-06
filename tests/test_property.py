from hypothesis import given, strategies as st
from tasks import generate_unique_id, filter_tasks_by_priority

# generate_unique_id never returns an ID that's already in the list
@given(st.lists(st.integers(min_value=1, max_value=1000)))
def test_generate_unique_id_is_unique(ids):
    tasks = [{"id": i} for i in ids]
    new_id = generate_unique_id(tasks)
    assert new_id not in ids

# filtering preserves subset property
@given(
    tasks=st.lists(st.fixed_dictionaries({
        "id": st.integers(min_value=1, max_value=100),
        "priority": st.sampled_from(["High", "Medium", "Low"])
    }), unique_by=lambda d: d["id"]),
    prio=st.sampled_from(["High", "Medium", "Low"])
)
def test_filter_subset(tasks, prio):
    out = filter_tasks_by_priority(tasks, prio)
    in_ids  = {t["id"] for t in tasks}
    out_ids = {t["id"] for t in out}
    # result IDs must be a subset of input IDs
    assert out_ids.issubset(in_ids)
    # all returned tasks must match the priority
    assert all(t["priority"] == prio for t in out)
