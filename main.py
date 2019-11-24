#!/usr/bin/python3
import sys

from src.modules.mumjolandia.mumjolandia_starter import MumjolandiaStarter

commands = sys.argv[1:]
if not len(commands):
    commands = None
m = MumjolandiaStarter(commands)
m.run_cli()
