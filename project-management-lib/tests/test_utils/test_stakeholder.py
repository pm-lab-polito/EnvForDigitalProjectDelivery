import pytest

from utils.stakeholder import AbstractBaseStakeholder


def test_AbstractBaseStakeholder_raises_when_not_subclassed():
    with pytest.raises(TypeError):
        AbstractBaseStakeholder(
            first_name="fake_first_name",
            last_name="fake_last_name",
            email="fake_email",
        )


def test_AbstractBaseStakeholder():
    class Stakeholder(AbstractBaseStakeholder):
        def get_full_name(self):
            return "%s %s" % (self.first_name, self.last_name)

    stakeholder = Stakeholder(
        first_name="fake_first_name",
        last_name="fake_last_name",
        email="fake_email",
    )

    assert stakeholder.first_name == "fake_first_name"
    assert stakeholder.last_name == "fake_last_name"
    assert stakeholder.email == "fake_email"
    assert stakeholder.get_full_name() == "fake_first_name fake_last_name"
