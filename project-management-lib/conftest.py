import pytest
from pytest_factoryboy import register

from project.deliverables import Deliverable
from tests.factories import StakeholderFactory, WBSItemFactory

"""
fixture to be accessed with "stakeholder_factory" for access to the main object itself
or "stakeholder" to return an instance of the Stakeholder class
"""
register(StakeholderFactory)

register(WBSItemFactory)


@pytest.fixture
def deliverable():
    yield Deliverable(doc_title="Fake Deliverable")
