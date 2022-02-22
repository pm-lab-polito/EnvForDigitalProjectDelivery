import re

from .helpers import RiskCounterMeasure, RiskImpact, RiskProbabilty, RiskScore


class RiskMetaClass(type):
    pattern = r"^(rare|unlikely|moderate|likely|certain)_probability_(high|medium|low)_impact$"

    def __getattr__(cls, attr):
        if not re.match(cls.pattern, attr):
            raise AttributeError("'%s' object has no attribute '%s'" % (cls.__name__, attr))

        return lambda risk_name: cls.__get_risk_class(attr, risk_name)

    def __get_risk_class(cls, attr: str, risk_name: str):
        probability, _, impact, _ = attr.split("_")
        probability_value = RiskProbabilty[probability.upper()].value
        impact_value = RiskImpact[impact.upper()].value
        return Risk(risk_name, probability_value, impact_value)


class Risk(metaclass=RiskMetaClass):
    def __init__(self, risk_name: str, probability: int, impact: int):
        """
        :param name: Name of the Risk instance
        :type name: str
        :param probability: A value between 0 and 100 where each point denotes a percentage point
        :type probability: int
        :param impact: A value between 0 and 100 where each point denotes a percentage point
        :type impact: int
        """
        self.risk_name = risk_name
        self.impact = impact
        self.probability = probability
        self._risk_owner = None
        self._description = None
        self._counter_measure = None

    def get_risk_score(self):
        return RiskScore.get_risk_score(int(self.probability / 100 * self.impact))

    @property
    def risk_owner(self):
        return self._risk_owner

    @risk_owner.setter
    def risk_owner(self, value):
        self.assign_risk_owner(value)

    def assign_risk_owner(self, value):
        self._risk_owner = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def probability(self) -> int:
        return self._probability

    @probability.setter
    def probability(self, value: int):
        """
        :param value: An integer between 0 and 100 where each point denotes a percentage point
        :type value: int
        """
        assert value in range(101), "Please pass an integer between 0 and 100"
        self._probability = value

    @property
    def impact(self) -> int:
        return self._impact

    @impact.setter
    def impact(self, value: int):
        """
        :param value: An integer between 0 and 100 where each point denotes a percentage point
        :type value: int
        """
        assert value in range(101), "Please pass a number between 0 and 1"
        self._impact = value

    @property
    def counter_measure(self):
        return self._counter_measure

    @counter_measure.setter
    def counter_measure(self, value):
        self.set_counter_measure(value)

    def set_counter_measure(self, counter_measure: str):
        """counter_measure is a value to be chosen from the RiskCounterMeasure Enum"""
        allowed_values = RiskCounterMeasure.list_allowed_values()
        assert counter_measure.upper() in allowed_values, "%s is not in %s" % (
            counter_measure,
            allowed_values,
        )
        self._counter_measure = RiskCounterMeasure(counter_measure.upper())
