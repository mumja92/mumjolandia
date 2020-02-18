from unittest import TestCase
from unittest.mock import patch

import logging

from tests.ut.helpers.helpers import DateTimeHelper


class TestPeriodicTaskProgressHandler(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPeriodicTaskProgressHandler, self).__init__(*args, **kwargs)
        logging.getLogger().disabled = True

    def setUp(self):
        self.patcher_date_long = patch('src.utils.helpers.DateHelper.get_today_long')
        self.mock_date_long = self.patcher_date_long.start()
        self.mock_date_long.side_effect = lambda date_shift=0: DateTimeHelper.get_fixed_datetime(date_shift)
        self.addCleanup(self.patcher_date_long.stop)

        self.patcher_date_short = patch('src.utils.helpers.DateHelper.get_today_short')
        self.mock_date_short = self.patcher_date_short.start()
        self.mock_date_short.side_effect = lambda date_shift=0: DateTimeHelper.get_fixed_date(date_shift)
        self.addCleanup(self.patcher_date_short.stop)

        self.patcher_shared_preferences_get = patch('src.utils.shared_preferences.SharedPreferences.get')
        self.mock_shared_preferences_get = self.patcher_shared_preferences_get.start()
        self.mock_shared_preferences_get.side_effect = lambda date_shift=0: DateTimeHelper.get_fixed_date(date_shift)
        self.addCleanup(self.patcher_shared_preferences_get.stop)

        self.patcher_shared_preferences_put = patch('src.utils.shared_preferences.SharedPreferences.put')
        self.mock_shared_preferences_put = self.patcher_shared_preferences_put.start()
        self.mock_shared_preferences_put.side_effect = lambda date_shift=0: DateTimeHelper.get_fixed_date(date_shift)
        self.addCleanup(self.patcher_shared_preferences_put.stop)

        self.patcher_shared_preferences_clear = patch('src.utils.shared_preferences.SharedPreferences.clear_starting_pattern')
        self.mock_shared_preferences_clear = self.patcher_shared_preferences_clear.start()
        self.mock_shared_preferences_clear.side_effect = lambda date_shift=0: DateTimeHelper.get_fixed_date(date_shift)
        self.addCleanup(self.patcher_shared_preferences_clear.stop)

    test_data = []

    # todo: add tests
    # @patch.object(PeriodicTaskLoader, 'get', return_value=test_data)
    # def test_get_list_next_occurrence_ok(self, mock_load):
    #     ptph = PeriodicTaskProgressHandler('dummy')
