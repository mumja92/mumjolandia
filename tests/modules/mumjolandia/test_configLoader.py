import logging
import os
from unittest import TestCase

from src.modules.mumjolandia.config_loader import ConfigLoader


class TestConfigLoader(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestConfigLoader, self).__init__(*args, **kwargs)
        logging.getLogger().disabled = True

    def test_get_config_correct_file_non_default_values(self):
        with open("configLoader.xml", "w+") as f:
            f.write("""<config>
            <!--'CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET'-->
            <log_level>error</log_level>
            <!--'True, False'-->
            <log_to_display>false</log_to_display>
            <!--'True, False'-->
            <log_to_file>true</log_to_file>
            <!--'xml, pickle'-->
            <task_io_method>pickle</task_io_method>
            <!--'xxx.xxx.xxx.xxx'-->
            <server_address>192.168.0.100</server_address>
            <!--'1024-65535'-->
            <server_port>1234</server_port>
            </config>""")
        config = ConfigLoader.get_config("configLoader.xml")
        self.assertEqual(config.log_level.lower(), 'error')
        self.assertEqual(config.log_to_display.lower(), 'false')
        self.assertEqual(config.log_to_file.lower(), 'true')
        self.assertEqual(config.task_io_method.lower(), 'pickle')
        self.assertEqual(config.server_address.lower(), '192.168.0.100')
        self.assertEqual(config.server_port.lower(), '1234')
        os.remove("configLoader.xml")

    def test_get_config_file_does_not_exist(self):
        config = ConfigLoader.get_config("configLoader.xml")
        self.assertEqual(config.log_level.lower(), 'warning')
        self.assertEqual(config.log_to_display.lower(), 'true')
        self.assertEqual(config.log_to_file.lower(), 'false')
        self.assertEqual(config.task_io_method.lower(), 'xml')
        self.assertEqual(config.server_address.lower(), '127.0.0.1')
        self.assertEqual(config.server_port.lower(), '3333')

    def test_get_config_empty_xml(self):
        with open("configLoader.xml", "w+") as f:
            f.write("""<config></config>""")
        config = ConfigLoader.get_config("configLoader.xml")
        self.assertEqual(config.log_level.lower(), 'warning')
        self.assertEqual(config.log_to_display.lower(), 'true')
        self.assertEqual(config.log_to_file.lower(), 'false')
        self.assertEqual(config.task_io_method.lower(), 'xml')
        self.assertEqual(config.server_address.lower(), '127.0.0.1')
        self.assertEqual(config.server_port.lower(), '3333')
        os.remove("configLoader.xml")

    def test_get_config_incorrect_xml_file(self):
        with open("configLoader.xml", "w+") as f:
            f.write("""<config><task></config>""")
        config = ConfigLoader.get_config("configLoader.xml")
        self.assertEqual(config.log_level.lower(), 'warning')
        self.assertEqual(config.log_to_display.lower(), 'true')
        self.assertEqual(config.log_to_file.lower(), 'false')
        self.assertEqual(config.task_io_method.lower(), 'xml')
        self.assertEqual(config.server_address.lower(), '127.0.0.1')
        self.assertEqual(config.server_port.lower(), '3333')
        os.remove("configLoader.xml")

    def test_get_config_values_out_of_enums(self):
        with open("configLoader.xml", "w+") as f:
            f.write("""<config>
            <!--'CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET'-->
            <log_level>wszystko</log_level>
            <!--'True, False'-->
            <log_to_display></log_to_display>
            <!--'True, False'-->
            <log_to_file>nie</log_to_file>
            <!--'xml, pickle'-->
            <task_io_method>binary</task_io_method>
            <!--'xxx.xxx.xxx.xxx'-->
            <server_address>kotek</server_address>
            <!--'1024-65535'-->
            <server_port>dzem</server_port>
        </config>""")
        config = ConfigLoader.get_config("configLoader.xml")
        self.assertEqual(config.log_level.lower(), 'warning')
        self.assertEqual(config.log_to_display.lower(), 'true')
        self.assertEqual(config.log_to_file.lower(), 'false')
        self.assertEqual(config.task_io_method.lower(), 'xml')
        self.assertEqual(config.server_address.lower(), '127.0.0.1')
        self.assertEqual(config.server_port.lower(), '3333')
        os.remove("configLoader.xml")

    def test_get_config_values_incorrect_server_values(self):
        with open("configLoader.xml", "w+") as f:
            f.write("""<config>
            <!--'xxx.xxx.xxx.xxx'-->
            <server_address>192.168.0</server_address>
            <!--'1024-65535'-->
            <server_port>1023</server_port>
        </config>""")
        config = ConfigLoader.get_config("configLoader.xml")
        self.assertEqual(config.server_address.lower(), '127.0.0.1')
        self.assertEqual(config.server_port.lower(), '3333')
        os.remove("configLoader.xml")

        with open("configLoader.xml", "w+") as f:
            f.write("""<config>
            <!--'xxx.xxx.xxx.xxx'-->
            <server_address>100.x.x.x</server_address>
            <!--'1024-65535'-->
            <server_port>65536</server_port>
        </config>""")
        config = ConfigLoader.get_config("configLoader.xml")
        self.assertEqual(config.server_address.lower(), '127.0.0.1')
        self.assertEqual(config.server_port.lower(), '3333')
        os.remove("configLoader.xml")

        with open("configLoader.xml", "w+") as f:
            f.write("""<config>
            <!--'xxx.xxx.xxx.xxx'-->
            <server_address></server_address>
            <!--'1024-65535'-->
            <server_port>1000.5</server_port>
        </config>""")
        config = ConfigLoader.get_config("configLoader.xml")
        self.assertEqual(config.server_address.lower(), '127.0.0.1')
        self.assertEqual(config.server_port.lower(), '3333')
        os.remove("configLoader.xml")
