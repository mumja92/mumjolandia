import logging
from unittest import TestCase

from src.interface.planner.plan import Plan


class TestPlan(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPlan, self).__init__(*args, **kwargs)
        logging.getLogger().disabled = True

    def test_add_different_time_ok(self):
        plan = Plan(0)
        self.assertTrue(plan.add_task("name", 30, "9:00"))
        self.assertTrue(plan.add_task("name", 60, "09:30"))
        self.assertTrue(plan.add_task("name", 10, "08:30"))

    def test_add_task_in_time_of_other_task_nook(self):
        plan = Plan(0)
        self.assertTrue(plan.add_task("name", 90, "9:00"))
        self.assertFalse(plan.add_task("name", 60, "09:01"))
        self.assertFalse(plan.add_task("name", 60, "10:29"))

    def test_add_task_before_existing_but_duration_too_long_nook(self):
        plan = Plan(0)
        self.assertTrue(plan.add_task("name", 90, "11:00"))
        self.assertFalse(plan.add_task("name", 60, "10:30"))
        self.assertTrue(plan.add_task("name", 30, "10:30"))
