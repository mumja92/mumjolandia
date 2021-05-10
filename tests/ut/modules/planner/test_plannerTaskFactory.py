import logging
from unittest import TestCase

from src.modules.planner.planner_task_factory import PlannerTaskFactory


class TestPlannerTaskFactory(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPlannerTaskFactory, self).__init__(*args, **kwargs)
        logging.getLogger().disabled = True

    def test_get_ok(self):
        self.assertIsNotNone(PlannerTaskFactory().get('10:30', 1, 'test'))

    def test_get_no_ok(self):
        self.assertIsNone(PlannerTaskFactory().get('30:30', 1, 'test'))
        self.assertIsNone(PlannerTaskFactory().get('14:3', 1, 'test'))
        self.assertIsNone(PlannerTaskFactory().get('14:a2', 1, 'test'))
        self.assertIsNone(PlannerTaskFactory().get('15:15', -1, 'test'))
