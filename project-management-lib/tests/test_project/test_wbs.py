from datetime import datetime, timedelta
from typing import List

import pytest

from project.wbs import WBS, Node
from project.wbs_item import WBSItem

WBS_NAME = "Fake WBS"
FIXED_START_DATE = datetime(2022, 1, 14, 11, 26, 3)


@pytest.fixture
def wbs():
    yield WBS(name=WBS_NAME, start_date=FIXED_START_DATE)


def test_WBS(wbs: WBS):
    assert str(wbs) == WBS_NAME == wbs.name
    assert wbs.wbs_items == []
    assert wbs.start_date == FIXED_START_DATE
    assert wbs.finish_date == "N/A"
    assert wbs.get_critical_path() is None
    assert isinstance(wbs.parent_node, Node)

    with pytest.raises(AssertionError):
        """
        Accessing this atribute before adding WBSItems should raise an assertion error
        """
        assert wbs.percent_complete


def test_WBS_add_items(wbs: WBS, wbs_item_factory):
    number_of_items = 100
    wbs_items: List[WBSItem] = wbs_item_factory.build_batch(number_of_items)
    wbs.add_wbs_item(*wbs_items)
    assert wbs.percent_complete == sum(x.percent_complete for x in wbs_items) // number_of_items
    assert wbs.wbs_items == wbs_items
    assert len(wbs.wbs_items) == number_of_items


def test_WBS_link_nodes(wbs: WBS, wbs_item_factory):
    node1 = wbs_item_factory.build(work_item_name="node1", duration=timedelta(days=5))
    node2 = wbs_item_factory.build(work_item_name="node2", duration=timedelta(days=3))
    node3 = wbs_item_factory.build(work_item_name="node3", duration=timedelta(days=2))
    node4 = wbs_item_factory.build(work_item_name="node4", duration=timedelta(days=9))
    node5 = wbs_item_factory.build(work_item_name="node5", duration=timedelta(days=6))
    node6 = wbs_item_factory.build(work_item_name="node6", duration=timedelta(days=8))
    node7 = wbs_item_factory.build(work_item_name="node7", duration=timedelta(days=4))

    # must call `.add_wbs_item()` first and add all items
    wbs.add_wbs_item(node1, node2, node3, node4, node5, node6, node7)
    assert len(wbs.wbs_items) == 7

    wbs.add_wbs_item(node1, node2)  # duplicate not added
    assert len(wbs.wbs_items) == 7

    # assuming the graph is this below

    #             /‾node3‾‾‾‾‾‾‾‾‾‾‾‾‾node6
    #            /                 /      \
    # node1---node2-------node4---        node7
    #             \           \          /
    #              \__________node5_____/

    # The corresponding node pairs is this below
    node_pairs = (
        (node1, node2),
        (node2, node3),
        (node3, node6),
        (node6, node7),
        (node2, node4),
        (node4, node6),
        (node2, node5),
        (node4, node5),
        (node5, node7),
    )
    wbs.link_nodes(*node_pairs)
    assert wbs.duration.days == 29
    assert wbs.get_critical_path() == "node1 -> node2 -> node4 -> node6 -> node7"

    # test cannot call `.link_nodes() with a node not added to wbs_items
    node8 = wbs_item_factory.build(work_item_name="node8", duration=timedelta(days=4))
    node9 = wbs_item_factory.build(work_item_name="node9", duration=timedelta(days=44))
    with pytest.raises(KeyError):
        wbs.link_nodes((node8, node9))
