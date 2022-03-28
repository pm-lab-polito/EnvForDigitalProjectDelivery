from abc import ABC
from datetime import datetime, timezone


class AbstractBaseDocument(ABC):
    def __init__(self, doc_title) -> None:
        super().__init__()
        self.doc_title = doc_title
        self.time_created = datetime.now(tz=timezone.utc)
