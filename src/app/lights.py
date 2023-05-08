# panda3d imports
from panda3d.core import (AmbientLight, Spotlight, PointLight, Vec3)

__author__ = "Jonty Doyle"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "21 September 2022"

LIGHT_HEIGHT = 100


class Lights:
    """Defines lighting for rendered model"""

    def __init__(self, base):
        self.base = base
        self.__set_lights()

    def __set_lights(self):
        """Sets default lighting"""
        self.__set_ambient_light()
        self.__set_down_light(0.8, LIGHT_HEIGHT)
        self.__set_point_light(0.6)

    def __set_ambient_light(self):
        """Sets light as ambient as defined in panda3d"""
        a = AmbientLight('ambient-light')
        a.setColor((0.2, 0.2, 0.2, 1))
        node = self.base.render.attachNewNode(a)
        node.setZ(LIGHT_HEIGHT)
        self.base.render.setLight(node)

    def __set_down_light(self, strength, height):
        """Sets direction of down light as defined by panda3d"""
        p = PointLight('down-light')

        p.setShadowCaster(True, 512, 512)
        p.setColor((strength, strength, strength, 1))

        node = self.base.render.attachNewNode(p)
        node.setZ(height)
        node.lookAt(0, 0, 0)
        self.base.render.setLight(node)

    def __set_point_light(self, strength):
        """Sets direction of point light light as defined by panda3d"""
        p = PointLight('point-light')
        p.setColor((strength, strength, strength, 1))

        self.light_node = self.base.render.attachNewNode(p)
        self.base.render.setLight(self.light_node)

    def update(self, config):
        """Updates model lighting.
        Typically used when model is created or cleared."""
        self.light_node.setPos(-config.x, -config.y, LIGHT_HEIGHT)
        self.light_node.lookAt(0, 0, 0)
