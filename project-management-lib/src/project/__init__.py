from src.project.project_charter import ProjectCharter

from .deliverables import Deliverable
from .governance import ProjectGovernance


class Project:
    def __init__(self, project_charter) -> None:
        self.project_charter: ProjectCharter = project_charter
        self.stakeholders = project_charter.project_stakeholders
        self._deliverables = []
        self._project_risks = []
        self.project_governance = ProjectGovernance(self)

    @property
    def deliverables(self):
        return self._deliverables

    @property
    def project_risks(self):
        return self._project_risks

    def add_new_project_risk(self, risk):
        assert risk not in self._project_risks, "This Risk already exists within the current project"
        self._project_risks.append(risk)

    def add_deliverable(self, value: Deliverable):
        assert value not in self._deliverables, "This Deliverable already exists within the project"
        self._deliverables.append(value)

    def create_deliverable(self, deliverable_name):
        deliverable = Deliverable(deliverable_name)
        self.add_deliverable(deliverable)
        return deliverable

    def accept_deliverable(self, deliverable: Deliverable):
        assert deliverable in self._deliverables, "Deliverable does not exist within the current project"
        deliverable.mark_as_accepted()

    def reject_deliverable(self, deliverable: Deliverable):
        assert deliverable in self._deliverables, "Deliverable does not exist within the current project"
        deliverable.mark_as_rejected()

    def __repr__(self) -> str:
        return self.project_charter.project_title
