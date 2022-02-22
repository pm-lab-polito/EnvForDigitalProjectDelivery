from unittest.mock import Mock

import pytest

from project.governance import ProjectGovernance


@pytest.fixture
def governance(stakeholder_factory, monkeypatch):
    stakeholders = stakeholder_factory.create_batch(5)

    mock_project_charter = Mock(spec=["project_stakeholders"])
    monkeypatch.setattr(mock_project_charter, "project_stakeholders", stakeholders, raising=True)

    mock_project = Mock(spec=["project_charter"])
    monkeypatch.setattr(mock_project, "project_charter", mock_project_charter, raising=True)

    governance = ProjectGovernance(project=mock_project)

    yield governance


def test_ProjectGovernance(governance, monkeypatch):
    stakeholders = governance.get_all_stakeholders()

    assert stakeholders == governance.not_signed_by

    terms = "Some terms and conditions"
    monkeypatch.setattr(governance, "TERMS_N_CONDITIONS", terms, raising=True)
    assert governance.TERMS_N_CONDITIONS == terms

    assert not governance.signed_by
    assert not governance.signed_by_all

    for stakeholder in stakeholders:
        governance.sign_agreement(stakeholder)

    assert governance.signed_by_all
    assert governance.signed_by == stakeholders


def test_external_stakeholder_cannot_sign(governance, stakeholder):
    with pytest.raises(AssertionError):
        governance.sign_agreement(stakeholder)


def test_stakeholder_cannot_sign_twice(governance):
    stakeholders = governance.get_all_stakeholders()
    governance.sign_agreement(stakeholders[0])

    with pytest.raises(AssertionError):
        governance.sign_agreement(stakeholders[0])

    assert len(governance.signed_by) == len(stakeholders) - len(governance.not_signed_by)


def test_only_stakeholder_instances_allowed_to_sign(governance):
    not_stakeholder_instance = Mock()

    with pytest.raises(AssertionError):
        governance.sign_agreement(not_stakeholder_instance)
