from enum import Enum


class RiskProbabilty(Enum):
    """
    Characterizes the likelihood that a particular risk arises during a particular project

    Some arbitrary values are defined here and the upper bounds chosen

    * RARE = 0% < x ≤ 5%
    * UNLIKELY = 5% < x ≤ 29%
    * POSSIBLE = 30% < x ≤ 50%
    * LIKELY = 50% < x ≤ 80%
    * CERTAIN = 80% < x ≤ 100%
    """

    RARE = 5
    UNLIKELY = 30
    MODERATE = 50
    LIKELY = 80
    CERTAIN = 100


class RiskImpact(Enum):
    """Defines how a particular risk can affect the progress of a project"""

    HIGH = 100
    MEDIUM = 50
    LOW = 10


class RiskScore(Enum):
    VERY_HIGH = range(80, 101)  # 80% - 100%
    HIGH = range(50, 80)  # 50% - 79%
    MODERATE = range(30, 50)  # 30% - 49%
    LOW = range(0, 30)  # 0 - 29%

    @classmethod
    def get_risk_score(cls, value):
        for val in cls:
            if value in val.value:
                return val


class RiskCounterMeasure(Enum):
    REDUCE = "REDUCE"
    PREVENT = "PREVENT"
    ACCEPT = "ACCEPT"
    TRANSFER = "TRANSFER"

    @classmethod
    def list_allowed_values(cls):
        return list(map(lambda c: c.value, cls))
