from project.deliverables import Deliverable
from project.project_stakeholder import Stakeholder


def test_Deliverable(deliverable: Deliverable, monkeypatch):
    """
    :param deliverable: comes from conftest.py at the root
    :type deliverable: Deliverable
    :param monkeypatch: pytest fixture for patching on the fly
    """
    assert deliverable.doc_title == "Fake Deliverable"
    assert deliverable.accepted == "N/A"
    assert deliverable.description is None
    assert deliverable.acceptance_criteria is None
    assert deliverable.expected_result is None
    assert deliverable.reviewer is None

    monkeypatch.setattr(deliverable, "description", "Fake Description", raising=True)
    assert deliverable.description == "Fake Description"

    monkeypatch.setattr(deliverable, "acceptance_criteria", "Fake Criteria", raising=True)
    assert deliverable.acceptance_criteria == "Fake Criteria"

    monkeypatch.setattr(deliverable, "expected_result", "Fake Result", raising=True)
    assert deliverable.expected_result == "Fake Result"


def test_can_set_deliverable_reviewer(deliverable: Deliverable, stakeholder: Stakeholder):
    deliverable.set_reviewer(stakeholder)
    assert deliverable.reviewer is stakeholder


def test_can_accept_deliverable(deliverable: Deliverable):
    deliverable.mark_as_accepted()
    assert deliverable.accepted is True


def test_can_reject_deliverable(deliverable: Deliverable):
    deliverable.mark_as_rejected()
    assert deliverable.accepted is False
