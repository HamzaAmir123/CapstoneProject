from direct.showbase.ShowBase import ShowBase
from panda3d.core import AntialiasAttrib
from .ui.base import BaseUI

from .app import App


class App(ShowBase):

    def __init__(self):

        super().__init__(self)
        self.bindings = Keybindings(self)
        self.lights = Lights(self)
        self.ui = BaseUI(self)
        self.environment = Environment(self, self.ui)
        self.camera = Camera(self)


        self.environment.load("../../config/stress/config100.txt",
                              "../../config/stress/positions100.txt",
                              "../../data/starfish.json")
        print(self.environment.render_time)
        self.environment.clear()

        # Set defaults
        self.__set_defaults()

        # Set Keybindings
        self.bindings.set(self.environment, self.camera, self.ui)

    # Sets some defaults
    def __set_defaults(self):
        self.setBackgroundColor(0.9, 0.9, 0.9)
        self.render.setShaderAuto()
        self.render.setAntialias(AntialiasAttrib.MLine)  # Not sure
