from datetime import timedelta

from criticalpath import Node as N


class Node(N):
    def __init__(self, name, duration=None, lag=timedelta(0)):
        super().__init__(name, duration=duration, lag=lag)
