from unittest.mock import Mock

import pytest

from project.project_stakeholder import Stakeholder
from tests.faker import faker

FIRST_NAME = faker.first_name()
LAST_NAME = faker.last_name()
EMAIL = "{}{}@example.com".format(FIRST_NAME, LAST_NAME).lower()
RESPONSIBILITY = faker.text()
TITLE = faker.job()


@pytest.fixture
def stakeholder(stakeholder_factory):
    yield stakeholder_factory.build(first_name=FIRST_NAME, last_name=LAST_NAME)


def test_Stakeholder(stakeholder: Stakeholder):
    assert isinstance(stakeholder, Stakeholder)
    assert stakeholder.first_name == FIRST_NAME
    assert stakeholder.last_name == LAST_NAME
    assert stakeholder.email == EMAIL
    assert not stakeholder.projects_involved
    assert stakeholder.stakeholder_type == "unknown"
    assert stakeholder.role == "UNSET"
    assert str(stakeholder) == f"Stakeholder({stakeholder.first_name})"
    assert stakeholder.get_full_name() == f"{stakeholder.first_name} {stakeholder.last_name}"


@pytest.mark.parametrize("attr", ["responsibility", "stakeholder_title"])
def test_Stakeholder_attr_raises_when_not_set(attr, stakeholder):
    with pytest.raises(AttributeError):
        getattr(stakeholder, attr)


@pytest.mark.parametrize("attr, value", [("responsibility", RESPONSIBILITY), ("stakeholder_title", TITLE)])
def test_Stakeholder_attr_not_raises_when_set(attr, value, stakeholder):
    setattr(stakeholder, attr, value)
    assert getattr(stakeholder, attr) == value


@pytest.mark.parametrize(
    "attr, value",
    [("stakeholder_type", "not_allowed_value"), ("role", "not_allowed_value")],
)
def test_Stakeholder_cannot_set_attr_not_in_allowed_values(attr, value, stakeholder):
    with pytest.raises(AssertionError):
        setattr(stakeholder, attr, value)


@pytest.mark.parametrize("allowed_value", ["professor", "student", "unknown"])
def test_Stakeholder_can_set_type_in_allowed_values(allowed_value, stakeholder):
    setattr(stakeholder, "stakeholder_type", allowed_value)
    assert getattr(stakeholder, "stakeholder_type") == allowed_value


@pytest.mark.parametrize("allowed_value", ["R", "A", "C", "I"])
def test_Stakeholder_can_set_role_in_allowed_values(allowed_value, stakeholder):
    setattr(stakeholder, "role", allowed_value)
    assert getattr(stakeholder, "role") == allowed_value


def test_add_project_to_stakeholder(stakeholder: Stakeholder):
    fake_project1 = Mock()
    fake_project2 = Mock()
    stakeholder.add_to_involved_projects(fake_project1)
    assert stakeholder.get_number_of_projects() == 1
    stakeholder.add_to_involved_projects(fake_project2)
    assert stakeholder.get_number_of_projects() == 2
