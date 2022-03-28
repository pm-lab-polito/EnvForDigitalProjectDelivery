import random
from datetime import timedelta

import factory

from project.project_stakeholder import Stakeholder
from project.wbs_item import WBSItem

from .faker import faker


class StakeholderFactory(factory.Factory):
    class Meta:
        model = Stakeholder

    first_name = factory.LazyAttribute(lambda _: faker.unique.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.unique.last_name())
    email = factory.LazyAttribute(lambda self: "{}{}@example.com".format(self.first_name, self.last_name).lower())


class WBSItemFactory(factory.Factory):
    class Meta:
        model = WBSItem

    work_item_name = factory.LazyAttribute(lambda _: faker.unique.text().split(" ")[0])
    duration = factory.LazyAttribute(lambda _: timedelta(days=random.randint(0, 365)))

    @factory.post_generation
    def add_percent_complete(self, create, extracted, **kwargs):
        self.percent_complete = random.randint(1, 100)
