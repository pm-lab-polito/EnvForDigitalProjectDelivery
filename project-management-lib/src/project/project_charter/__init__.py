from typing import List, Optional, Union

from src.utils import AbstractBaseDocument

from ..project_stakeholder import Stakeholder


class ProjectCharter(AbstractBaseDocument):
    """
    A project is defined by a project charter.
    Once a project charter exists, it is assumed that a project is underway
    """

    def __init__(self, project_title: Optional[str] = None) -> None:
        super().__init__("Project Charter")
        self._project_title = project_title
        self._project_stakeholders: List[Stakeholder] = []
        self._executive_summary = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._project_title})"

    @property
    def project_title(self):
        return self._project_title

    @project_title.setter
    def project_title(self, value: str):
        self._project_title = value

    @property
    def executive_summary(self):
        return self._executive_summary

    @executive_summary.setter
    def executive_summary(self, value: str):
        self._executive_summary = value

    @property
    def project_stakeholders(self) -> List[Stakeholder]:
        return self._project_stakeholders

    def add_stakeholder(self, stakeholder: Union[Stakeholder, List[Stakeholder]]):
        assert self.is_class_stakeholder(stakeholder), (
            "Only Stakeholder instances can be added, not %s." % type(stakeholder).__name__
        )
        if isinstance(stakeholder, (list, tuple)):
            for s in stakeholder:
                self.__finalize_add_stakeholder(s)
        else:
            self.__finalize_add_stakeholder(stakeholder)

    def __finalize_add_stakeholder(self, stakeholder: Stakeholder):
        assert stakeholder not in self._project_stakeholders, (
            'This Stakeholder "%s" already exists within the charter' % stakeholder.get_full_name()
        )
        self._project_stakeholders.append(stakeholder)
        stakeholder.add_to_involved_projects(self)

    @staticmethod
    def is_class_stakeholder(obj) -> bool:
        """
        Checks that the stakeholder about to be added to the project
        is instance of the Stakeholder class
        """
        if isinstance(obj, list):
            return all(isinstance(s, Stakeholder) for s in obj)
        return isinstance(obj, Stakeholder)
