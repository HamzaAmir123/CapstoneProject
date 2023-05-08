"""App module. For RoboViz application"""


import sys
import os
import atexit
from pathlib import Path

from direct.showbase.ShowBase import ShowBase
from panda3d.core import AntialiasAttrib

from .ui.base import BaseUI
from .logger import Logger
from .camera import Camera
from .keybindings import Keybindings
from .lights import Lights
from .environment import Environment

__author__ = "Jonty Doyle"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "21 September 2022"

DATA_ENV = "ROBOVIZ_HOME"  # Environment Variable referring to Data Location
DIR_NAME = ".roboviz"  # Default directory name


class App(ShowBase):
    """Application base which creates model parent node to which everything
    is attached. Inherits from panda3d ShowBase class (inital render)"""

    def __init__(self, args):
        super().__init__(self)
        self.DATA_DIR = self.__get_data_dir()
        self.logger = Logger(self.DATA_DIR)
        atexit.register(self.logger.write)

        # Create RoboViz model manipulation objects
        self.lights = Lights(self)
        self.ui = BaseUI(self)
        self.camera = Camera(self)
        self.environment = Environment(self)
        self.bindings = Keybindings(self)

        # Set defaults
        self.__set_defaults()

        # Set Keybindings & Refresh UI
        self.ui.refresh()
        self.bindings.update()

    def handle_arguments(self, args):
        # Prints currently saved models
        parse = self.ui.console.parse

        if args.list:
            [print(env) for env in self.environment.envs]
            sys.exit(0)
        # Opens specified saved model
        elif args.load:
            cmd = ["load", args.load]
            parse(" ".join(cmd))
        # Sets model parameters if application run from command line.
        elif (args.config and args.position and args.data):
            cmd = ["open", args.config, args.position, args.data]
            parse(" ".join(cmd))
        else:
            pass

        if args.cmd:
            cmd = args.cmd.split(" ")
            parse(" ".join(cmd))

    def __set_defaults(self):
        """Sets defaults for model rendering"""
        self.setBackgroundColor(0.85, 0.86, 0.87)
        self.render.setShaderAuto()
        self.render.setAntialias(AntialiasAttrib.MLine)  # Not sure

    def __get_data_dir(self) -> Path:
        """Sets data location and returns path."""
        if DATA_ENV in os.environ:
            root = Path(os.environ[DATA_ENV])
            path = root / DIR_NAME
        else:
            path = Path.cwd() / DIR_NAME

        path = path.expanduser()

        if not path.is_dir():
            try:
                path.mkdir(exist_ok=True)
                print(f'Created data directory: "{path}"')
            except FileNotFoundError as e:
                print(e)

        return path
