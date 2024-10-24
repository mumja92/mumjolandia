from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from tests.utils.MumjolandiaTest import MumjolandiaTest


class TestUtilsSupervisor(MumjolandiaTest):
    def __init__(self, *args, **kwargs):
        super(TestUtilsSupervisor, self).__init__(*args, **kwargs)

    def test_ip_get_ok(self):
        response = self.send_command("utils ip")
        self.assertEqual(response.status, MumjolandiaReturnValue.utils_get)
        self.assertEqual(all(part.isdigit() for part in response.arguments[0].split('.')) and len(response.arguments[0].split('.')) == 4, True)

    def test_location_get_ok(self):
        response = self.send_command("utils location")
        self.assertEqual(response.status, MumjolandiaReturnValue.utils_get)
        self.assertTrue(len(response.arguments[0]) > 0)
