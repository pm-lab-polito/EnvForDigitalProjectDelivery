from datetime import datetime
from typing import List, Tuple

from src.utils import Node

from ..wbs_item import WBSItem


class WBS:
    _check_update_called = False

    def __init__(self, name, start_date: datetime = datetime.now()) -> None:
        self.name = name
        self._wbs_items: List[WBSItem] = []
        self.start_date: datetime = start_date
        self.parent_node = Node(self.name)

    @property
    def percent_complete(self):
        assert self._wbs_items, "The WBS Items list is empty. Populate it to get the value of this attribute"
        return sum(x.percent_complete for x in self._wbs_items) // len(self._wbs_items)

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value: datetime):
        assert isinstance(value, datetime), "start_date takes a datetime object, not %s." % type(value).__name__
        self._start_date = value

    @property
    def finish_date(self):
        """This value depends on duration which depends on wbs_items not being empty"""
        return self.start_date + self.duration if self.duration else "N/A"

    @property
    def duration(self):
        self.update_all()
        return self.parent_node.duration

    @property
    def wbs_items(self):
        return self._wbs_items

    def update_all(self):
        """
        Updates timing calculations for all children nodes.
        Sets the es, ls, ef, lf information and updates duration
        """
        if not self._check_update_called and self.wbs_items:
            self._check_update_called = True
            self.parent_node.update_all()

    def get_critical_path(self):
        """calculate the critical path using CPM"""
        self.update_all()
        critical_path = self.parent_node.get_critical_path()
        return " -> ".join(str(x) for x in critical_path) if critical_path else None

    def add_wbs_item(self, *args: WBSItem):
        for wbs_item in args:
            assert isinstance(wbs_item, WBSItem), "Only WBSItem instances can be added, not %s." % (
                type(wbs_item).__name__,
            )
            if wbs_item in self._wbs_items:
                continue
            self._wbs_items.append(wbs_item)
            self.parent_node.add(wbs_item.node_instance)

    def link_nodes(self, *args: Tuple[WBSItem, WBSItem]):
        """
        links the WBSItems in a directed graph
        """
        initial = self.parent_node

        for pair in args:
            assert all(isinstance(x, WBSItem) for x in pair), "Only tuples of WBSItem instances are allowed"
            origin, dest = pair

            try:
                initial = initial.link(str(origin), str(dest))
            except KeyError as ke:
                raise KeyError(
                    f"The WBSItem {ke} does not exist within this WBS. "
                    "Did you forget to add it? add it using the method `.add_wbs_item()`"
                )

    def __repr__(self) -> str:
        return self.name
