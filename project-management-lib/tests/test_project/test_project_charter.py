from typing import List
from unittest.mock import Mock, call, patch

import pytest

from project.project_charter import ProjectCharter
from project.project_stakeholder import Stakeholder


@pytest.fixture
def charter():
    yield ProjectCharter(project_title="Fake Project")


def test_ProjectCharter(charter: ProjectCharter):
    assert charter.doc_title == "Project Charter"
    assert charter.project_title == "Fake Project"
    assert not charter.project_stakeholders
    assert not charter.executive_summary
    assert str(charter) == "ProjectCharter(Fake Project)"


def test_ProjectCharter_set_project_title(charter: ProjectCharter, monkeypatch):
    monkeypatch.setattr(charter, "project_title", "New Fake Project", raising=True)
    assert charter.project_title == "New Fake Project"


def test_ProjectCharter_set_executive_summary(charter: ProjectCharter, monkeypatch):
    monkeypatch.setattr(charter, "executive_summary", "Fake Summary", raising=True)
    assert charter.executive_summary == "Fake Summary"


def test_ProjectCharter_is_class_stakeholder(charter: ProjectCharter, stakeholder, stakeholder_factory):
    assert charter.is_class_stakeholder(stakeholder) is True

    stakeholders: List[Stakeholder] = stakeholder_factory.build_batch(5)
    assert charter.is_class_stakeholder(stakeholders) is True

    not_stakeholder = Mock()
    assert charter.is_class_stakeholder(not_stakeholder) is False

    altered_stakeholders = stakeholders.append(not_stakeholder)
    assert charter.is_class_stakeholder(altered_stakeholders) is False


def test_ProjectCharter__finalize_add_stakeholder(charter: ProjectCharter, stakeholder: Stakeholder):
    charter._ProjectCharter__finalize_add_stakeholder(stakeholder)
    assert stakeholder in charter.project_stakeholders
    assert charter in stakeholder.projects_involved


def test_ProjectCharter__finalize_add_stakeholder_cannot_add_stakeholder_twice(
    charter: ProjectCharter, stakeholder: Stakeholder
):
    charter._ProjectCharter__finalize_add_stakeholder(stakeholder)

    with pytest.raises(AssertionError):
        charter._ProjectCharter__finalize_add_stakeholder(stakeholder)


@patch("project.project_charter.ProjectCharter.is_class_stakeholder")
def test_ProjectCharter_add_stakeholder(mocked_is_class_stakeholder, charter: ProjectCharter, stakeholder_factory):
    assert charter.is_class_stakeholder is mocked_is_class_stakeholder
    stakeholders: List[Stakeholder] = stakeholder_factory.build_batch(5)

    mocked_is_class_stakeholder.return_value = False
    with pytest.raises(AssertionError):
        charter.add_stakeholder(stakeholders[0])

    mocked_is_class_stakeholder.return_value = True
    charter._ProjectCharter__finalize_add_stakeholder = Mock()
    charter.add_stakeholder(stakeholders[0])
    charter._ProjectCharter__finalize_add_stakeholder.assert_called_with(stakeholders[0])

    charter.add_stakeholder(stakeholders)
    expected_calls = (call(stakeholder) for stakeholder in stakeholders)
    charter._ProjectCharter__finalize_add_stakeholder.assert_has_calls(expected_calls)
