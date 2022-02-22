from enum import Enum


class StakeholderTypeEnum(Enum):
    """Add more stakeholder types to this class as needed"""

    PROFESSOR = "professor"
    STUDENT = "student"
    UNKNOWN = "unknown"

    @classmethod
    def list_allowed_values(cls):
        return list(map(lambda c: c.value, cls))


class RoleEnum(Enum):
    """
    This class is meant to model the responsibility roles in the RACI matrix model

    * R = Responsible
    Those who do the work to complete the task. There is at least one role with a participation type of responsible.

    * A = Accountable (also approver or final approving authority)
    The one who ensures the prerequisites of the task are met and who delegates the work.
    In other words, an accountable must sign off (approve) work that responsible provides.
    There must be only one accountable specified for each task or deliverable.

    * C = Consulted
    Those whose opinions are sought, typically subject-matter experts; and with whom there is two-way communication.

    * I = Informed
    Those who are kept up-to-date on progress, often only on completion of the task or deliverable.
    """

    RESPONSIBLE = "R"
    ACCOUNTABLE = "A"
    CONSULTED = "C"
    INFORMED = "I"
    UNSET = "UNSET"

    @classmethod
    def list_allowed_values(cls):
        return list(map(lambda c: c.value, cls))
