"""Entry point for RoboViz application"""

import sys
import argparse

# Imports application module
from .app import App

__author__ = "Jonty Doyle, Hamza Amir and Benjamin Chiddy"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "21 September 2022"


DESC = """RoboViz: A Robogen robot visualization platform.
       Load, save and view Robogen compatible models."""

# Provides command line help for user.
parser = argparse.ArgumentParser(
    description=(DESC))
parser.add_argument("-c", "--config", metavar=(""),
                    help="configuration file path", default=None)
parser.add_argument("-p", "--position", metavar=(""),
                    help="position file path", default=None)
parser.add_argument("-d", "--data", metavar=(""),
                    help="robots data file (.json)", default=None)
parser.add_argument("-l", "--list",
                    action='store_true',
                    help="list saved models to command line",
                    default=None)
parser.add_argument("-L", "--load",
                    metavar=(""),
                    help="load specified saved model",
                    default=None)
parser.add_argument("-C", "--cmd", metavar=(""),
                    help="Run a (single) roboviz command remotely", default=None)


def run():
    """Starts panda3d application starting with user interface"""
    args = parser.parse_args()
    app = App(args)

    app.handle_arguments(args)
    app.run()
