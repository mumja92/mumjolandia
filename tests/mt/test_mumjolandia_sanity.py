import os
import shutil
import logging

from unittest import TestCase
from src.modules.mumjolandia.mumjolandia_starter import MumjolandiaStarter
from src.utils.hidden_prints import HiddenPrints
from src.utils.object_loader_pickle import ObjectLoaderPickle


class TestMumjolandiaSanity(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMumjolandiaSanity, self).__init__(*args, **kwargs)
        logging.getLogger().disabled = True

    def setUp(self):
        self.mumjolandia_starter = MumjolandiaStarter()

    def tearDown(self):
        shutil.rmtree(os.path.abspath(os.curdir) + '/data')

    def test_translate(self):
        self.assertEqual(os.path.isfile('data/notes.pickle'), False)
        self.mumjolandia_starter.set_commands(["note add 'test note'", "note add 'second test note'", "exit"])
        with HiddenPrints():
            self.mumjolandia_starter.run_cli()
        self.mumjolandia_starter.get_mumjolandia_thread().join()
        self.assertEqual(os.path.isfile('data/notes.pickle'), True)
        note = ObjectLoaderPickle('data/notes.pickle').get()
        self.assertEqual(len(note), 2)
        self.assertEqual(str(note[0]), 'test note')
        self.assertEqual(str(note[1]), 'second test note')
