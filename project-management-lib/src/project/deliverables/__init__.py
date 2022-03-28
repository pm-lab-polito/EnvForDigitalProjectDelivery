from src.utils import AbstractBaseDocument


class Deliverable(AbstractBaseDocument):
    def __init__(self, doc_title) -> None:
        super().__init__(doc_title)
        self._description = None
        self._acceptance_criteria = None
        self._reviewer = None
        self._expected_result = None
        self._accepted = None

    @property
    def accepted(self):
        if not isinstance(self._accepted, bool):
            return "N/A"
        return self._accepted

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def acceptance_criteria(self):
        return self._acceptance_criteria

    @acceptance_criteria.setter
    def acceptance_criteria(self, value: str):
        self._acceptance_criteria = value

    @property
    def expected_result(self):
        return self._expected_result

    @expected_result.setter
    def expected_result(self, value: str):
        self._expected_result = value

    @property
    def reviewer(self):
        return self._reviewer

    def set_reviewer(self, value):
        """
        If the reviewer is internal to the project,
        value should be an instance of the Stakeholder class
        """
        self._reviewer = value

    def mark_as_accepted(self):
        self._accepted = True

    def mark_as_rejected(self):
        self._accepted = False
