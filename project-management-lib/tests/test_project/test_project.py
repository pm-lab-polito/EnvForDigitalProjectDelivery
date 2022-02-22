from unittest.mock import Mock

import pytest

from project import Project
from project.deliverables import Deliverable
from project.governance import ProjectGovernance


@pytest.fixture
def project(stakeholder_factory, monkeypatch):
    stakeholders = stakeholder_factory.create_batch(5)

    mock_project_charter = Mock(spec=["project_stakeholders", "project_title"])
    monkeypatch.setattr(mock_project_charter, "project_stakeholders", stakeholders, raising=True)
    monkeypatch.setattr(mock_project_charter, "project_title", "Fake Project", raising=True)

    project = Project(project_charter=mock_project_charter)

    yield project


def test_Project(project: Project):
    assert str(project) == "Fake Project"
    assert isinstance(project.project_charter, Mock)
    assert hasattr(project.project_charter, "project_stakeholders")
    assert hasattr(project.project_charter, "project_title")
    assert isinstance(project.project_governance, ProjectGovernance)
    assert project.deliverables == []
    assert project.project_risks == []


def test_Project_create_deliverable(project: Project):
    deliverable = project.create_deliverable(deliverable_name="Fake deliverable")

    assert isinstance(deliverable, Deliverable)
    assert len(project.deliverables) == 1
    assert project.deliverables[0] == deliverable


def test_Project_accept_reject_deliverable(project: Project):
    deliverable = project.create_deliverable(deliverable_name="Fake deliverable")
    project.accept_deliverable(deliverable=deliverable)
    assert deliverable.accepted is True

    project.reject_deliverable(deliverable=deliverable)
    assert deliverable.accepted is False


def test_Project_add_new_project_risk(project: Project):
    risk = Mock()
    assert project.project_risks == []
    project.add_new_project_risk(risk=risk)
    assert project.project_risks == [risk]
