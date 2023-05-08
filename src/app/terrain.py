from pathlib import Path

# panda3d imports
from panda3d.core import (AmbientLight, Spotlight, Fog, PointLight, NodePath,
                          Material)
from ..util import Color

__author__ = "Jonty Doyle"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "21 September 2022"

# Constants
BASE_DIR = Path(__file__).parents[2]
MODEL_DIR = BASE_DIR / 'assets' / 'models' / 'terrain' / 'egg'
SKY_SCALE = 50
GROUND_HEIGHT = 2


class Terrain:
    """Defines the terrain onto which robots are rendered in a model."""

    def __init__(self, base, config):
        self.base = base
        self.path = NodePath('Terrain')
        self.__set_terrain(config)
        self.bounds = self.path.getTightBounds()

    def __set_terrain(self, config):
        """Sets terrain defaults. Renders a large sqaure arena as terrain"""
        c = Color((59, 66, 82, 100))
        m = Material()
        m.setShininess(15)
        m.setRefractiveIndex(0.5)

        m.setDiffuse(c.darken(0.9))
        m.setEmission(c.darken(0.7))
        m.setSpecular(c.lighten(0.2))

        # Defines size of terrain based on config file
        model = self.base.loader.loadModel(f'{MODEL_DIR}/Cube')
        model.setScale(config.x, config.y, GROUND_HEIGHT)
        model.setZ(-GROUND_HEIGHT / 2)

        model.setMaterial(m)
        model.reparentTo(self.path)
