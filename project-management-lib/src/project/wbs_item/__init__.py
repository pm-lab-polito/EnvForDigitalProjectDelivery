from datetime import timedelta

from src.utils import Node


class WBSItem:
    def __init__(self, work_item_name: str, duration: timedelta, lag: timedelta = timedelta(days=0)) -> None:
        self.work_item_name: str = work_item_name
        self.duration: timedelta = duration
        self.lag: timedelta = lag
        self._percent_complete: int = 0
        self._status = None
        self._objective = None
        self._resource = None

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value: timedelta):
        assert not (
            hasattr(self, "duration") or hasattr(self, "__duration")
        ), "This attribute is immutable once the object is created"
        assert isinstance(value, timedelta), "Only timedelta objects can be set, not %s." % type(value).__name__

        self.__duration = value

    @duration.deleter
    def duration(self):
        raise Exception("This attribute is immutable")

    @property
    def lag(self):
        return self._lag

    @lag.setter
    def lag(self, value: timedelta):
        assert isinstance(value, timedelta), "Only timedelta objects can be set, not %s." % type(value).__name__
        self._lag = value

    @property
    def percent_complete(self):
        return self._percent_complete

    @percent_complete.setter
    def percent_complete(self, value: int):
        assert value in range(0, 101), "Enter a integer between 0 and 100"
        self._percent_complete = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def objective(self):
        return self._objective

    @objective.setter
    def objective(self, value):
        self._objective = value

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, value):
        self._resource = value

    @property
    def node_instance(self):
        return Node(name=self.work_item_name, duration=self.__duration, lag=self._lag)

    def __repr__(self) -> str:
        return self.work_item_name
