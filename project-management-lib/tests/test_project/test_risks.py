import pytest

from src.project.risks import Risk
from src.project.risks.helpers import RiskCounterMeasure, RiskImpact, RiskProbabilty, RiskScore
from tests.faker import faker


@pytest.fixture
def risk():
    yield Risk(risk_name="Fake Risk Name", probability=50, impact=100)


def test_create_Risk_object_directly(monkeypatch, stakeholder, risk):
    assert risk.risk_name == "Fake Risk Name"
    assert risk.impact == 100
    assert risk.probability == 50
    assert risk.risk_owner is None
    assert risk.description is None
    assert risk.counter_measure is None
    assert risk.get_risk_score() == RiskScore.HIGH
    assert isinstance(risk.get_risk_score(), RiskScore)

    monkeypatch.setattr(risk, "risk_owner", stakeholder, raising=True)
    assert risk.risk_owner == stakeholder

    monkeypatch.setattr(risk, "description", "Fake Description", raising=True)
    assert risk.description == "Fake Description"


def test_cannot_set_unallowed_counter_measure(risk):
    with pytest.raises(AssertionError):
        setattr(risk, "counter_measure", "Fake counter measure")
    assert risk.counter_measure is None


@pytest.mark.parametrize("counter_measure", ["ReDuce", "prevenT", "aCCepT", "transfer"])
def test_can_set_allowed_counter_measures_and_value_is_case_insensitive(counter_measure, risk):
    setattr(risk, "counter_measure", counter_measure)
    assert isinstance(risk.counter_measure, RiskCounterMeasure)
    assert risk.counter_measure == RiskCounterMeasure(counter_measure.upper())


@pytest.mark.parametrize("wrong_classmethod", ["not_a_real_classmethod", "maybe_probability_high_impact"])
def test_access_to_dynamic_classmethod_not_matched_by_regex_raises(wrong_classmethod):
    with pytest.raises(AttributeError):
        getattr(Risk, wrong_classmethod)


@pytest.mark.parametrize(
    "class_method",
    [
        "rare_probability_high_impact",
        "rare_probability_medium_impact",
        "rare_probability_low_impact",
        "unlikely_probability_high_impact",
        "unlikely_probability_medium_impact",
        "unlikely_probability_low_impact",
        "moderate_probability_high_impact",
        "moderate_probability_medium_impact",
        "moderate_probability_low_impact",
        "likely_probability_high_impact",
        "likely_probability_medium_impact",
        "likely_probability_low_impact",
        "certain_probability_high_impact",
        "certain_probability_medium_impact",
        "certain_probability_low_impact",
    ],
)
def test_access_to_dynamic_classmethod_matched_by_regex_will_not_raise(class_method):
    name = faker.unique.name()
    instance = getattr(Risk, class_method)(risk_name=name)

    assert instance.risk_name == name
    assert isinstance(instance.get_risk_score(), RiskScore)

    probability, _, impact, _ = class_method.split("_")
    probability_value = RiskProbabilty[probability.upper()].value
    impact_value = RiskImpact[impact.upper()].value

    assert instance.get_risk_score() == RiskScore.get_risk_score(int(probability_value / 100 * impact_value))
