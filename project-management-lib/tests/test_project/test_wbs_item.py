from datetime import timedelta

import pytest

from project.wbs_item import Node, WBSItem

NAME = "Fake WBSItem"
DURATION = timedelta(days=56)


@pytest.fixture
def wbs_item(wbs_item_factory):
    yield wbs_item_factory.build(work_item_name=NAME, duration=DURATION)


def test_WBSItem(wbs_item: WBSItem, monkeypatch):
    assert str(wbs_item) == NAME == wbs_item.work_item_name
    assert wbs_item.work_item_name == NAME
    assert wbs_item.duration == DURATION
    assert wbs_item.lag == timedelta(days=0)
    assert wbs_item.percent_complete != 0
    assert wbs_item.percent_complete in range(1, 101)
    assert wbs_item.status is None
    assert wbs_item.objective is None
    assert wbs_item.resource is None
    assert isinstance(wbs_item.node_instance, Node)

    monkeypatch.setattr(wbs_item, "percent_complete", 50, raising=True)
    assert wbs_item.percent_complete == 50

    monkeypatch.setattr(wbs_item, "status", "IN_PROGRESS", raising=True)
    assert wbs_item.status == "IN_PROGRESS"

    monkeypatch.setattr(wbs_item, "objective", "Fake objective", raising=True)
    assert wbs_item.objective == "Fake objective"

    monkeypatch.setattr(wbs_item, "resource", "Fake resource", raising=True)
    assert wbs_item.resource == "Fake resource"


def test_WBSItem_duration_cannot_be_deleted_or_modified(wbs_item: WBSItem):
    with pytest.raises(AssertionError):
        setattr(wbs_item, "duration", timedelta(days=4))

    with pytest.raises(Exception):
        delattr(wbs_item, "duration")
