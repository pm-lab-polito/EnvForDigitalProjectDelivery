from ..project_charter import ProjectCharter
from ..project_stakeholder import Stakeholder


class ProjectGovernance:
    TERMS_N_CONDITIONS = None

    def __init__(self, project) -> None:
        self._project = project
        self._signed_by = []
        self._project_charter: ProjectCharter = project.project_charter
        self._not_signed_by: list = self._project_charter.project_stakeholders[:]

    @property
    def signed_by(self) -> list:
        return self._signed_by

    @property
    def not_signed_by(self) -> list:
        return self._not_signed_by

    @property
    def signed_by_all(self) -> bool:
        return not bool(len(self._not_signed_by))

    def sign_agreement(self, signee: Stakeholder):
        assert isinstance(signee, Stakeholder), "Expected type Stakeholder, found %s" % type(signee).__name__

        assert signee in self.get_all_stakeholders(), (
            "%s can't sign as they are external to the project" % signee.get_full_name()
        )

        assert signee not in self._signed_by, "This document has already been signed by %s." % signee.get_full_name()
        self._signed_by.append(signee)
        self._not_signed_by.remove(signee)

    def get_all_stakeholders(self) -> list:
        return self._project_charter.project_stakeholders
