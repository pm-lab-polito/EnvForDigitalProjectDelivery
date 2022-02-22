from src.utils import AbstractBaseStakeholder

from .helpers import RoleEnum, StakeholderTypeEnum


class Stakeholder(AbstractBaseStakeholder):
    def __init__(self, first_name, last_name, email) -> None:
        super().__init__(first_name, last_name, email)
        self._stakeholder_type: StakeholderTypeEnum = StakeholderTypeEnum.UNKNOWN
        self._responsibility = None
        self._stakeholder_title = None
        self._role: RoleEnum = RoleEnum.UNSET
        self._projects_involved = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.first_name})"

    @property
    def stakeholder_type(self):
        return self._stakeholder_type.value

    @stakeholder_type.setter
    def stakeholder_type(self, value: str):
        allowed_values = StakeholderTypeEnum.list_allowed_values()
        assert value.lower() in allowed_values, 'Couldn\'t set property "stakeholder_type". "%s" is not in %s' % (
            value,
            allowed_values,
        )
        self._stakeholder_type = StakeholderTypeEnum(value.lower())

    @property
    def role(self):
        return self._role.value

    @role.setter
    def role(self, value: str):
        allowed_values = RoleEnum.list_allowed_values()
        assert value.upper() in allowed_values, 'Couldn\'t set property "role". "%s" is not in %s' % (
            value,
            allowed_values,
        )
        self._role = RoleEnum(value.upper())

    @property
    def responsibility(self):
        """A brief description of the stakeholder's designated activities"""
        if self._responsibility is None:
            raise AttributeError("This attribute is not set. call the setter to set it")
        return self._responsibility

    @responsibility.setter
    def responsibility(self, value: str):
        self._responsibility = value

    @property
    def stakeholder_title(self):
        if self._stakeholder_title is None:
            raise AttributeError("This attribute is not set. call the setter to set it")
        return self._stakeholder_title

    @stakeholder_title.setter
    def stakeholder_title(self, value: str):
        self._stakeholder_title = value

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def projects_involved(self):
        """A list of projects the current stakeholder is involved with"""
        return self._projects_involved

    def add_to_involved_projects(self, value):
        """
        This method should only be called by the `.__finalize_add_stakeholder()`
        method in the ProjectCharter class
        """
        self._projects_involved.append(value)

    def get_number_of_projects(self) -> int:
        return len(self._projects_involved)
