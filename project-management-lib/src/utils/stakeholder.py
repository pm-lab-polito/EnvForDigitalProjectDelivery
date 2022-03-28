from abc import ABC, abstractmethod


class AbstractBaseStakeholder(ABC):
    def __init__(self, first_name, last_name, email) -> None:
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    @abstractmethod
    def get_full_name(self):
        """an instance method to get the stakeholders full name"""
