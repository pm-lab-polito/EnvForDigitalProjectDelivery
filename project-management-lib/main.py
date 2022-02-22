from src.project import Project
from src.project.project_charter import ProjectCharter
from src.project.project_stakeholder import Stakeholder
from src.project.risks import Risk


class StakeholderType:
    STUDENT = "student"
    PROFESSOR = "professor"


class StakeholderRole:
    RESPONSIBLE = "R"
    ACCOUNTABLE = "A"
    CONSULTED = "C"
    INFORMED = "I"


student = Stakeholder("Chiemerie", "Ezechukwu", "student@studenti.polito.it")
student.stakeholder_type = StakeholderType.STUDENT
student.role = StakeholderRole.RESPONSIBLE

professor = Stakeholder("Prof. Paolo", "Demagistris", "professor@polito.it")
professor.stakeholder_type = StakeholderType.PROFESSOR
professor.role = StakeholderRole.ACCOUNTABLE

project_charter = ProjectCharter(project_title="Master's Thesis")
project_charter.add_stakeholder([student, professor])

external_stakeholder = Stakeholder("External", "External", "external@external.com")
project_charter.add_stakeholder(external_stakeholder)

project_charter2 = ProjectCharter(project_title="Another Master's Thesis")
project_charter2.add_stakeholder(professor)

# returns the number of projects a stakeholder is involved with
professor.get_number_of_projects()

# returns a list of the projects a stakeholder is involved with
professor.projects_involved

project = Project(project_charter)
deliverable = project.create_deliverable(deliverable_name="First Deliverable")
deliverable.set_reviewer(professor)
project.accept_deliverable(deliverable)

# The below method is one of 15 factory methods that can be used to create an instance of the Risk class
risk = Risk.moderate_probability_medium_impact(risk_name="Risk Name")
risk.set_counter_measure("reduce")

project.add_new_project_risk(risk)
