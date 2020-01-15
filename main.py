#!/usr/bin/python3
import sys

from src.modules.mumjolandia.mumjolandia_starter import MumjolandiaStarter

# todo: this file is not added to update package; it failed once because of this.
m = MumjolandiaStarter(sys.argv)
m.run_cli()
