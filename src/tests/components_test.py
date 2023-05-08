from ..component import CoreComponent, FixedBrick, ActiveHinge

from ..util import RobotData
from ..robot import Robot

DATA_PATH = "data"
MIN_PATH = f'{DATA_PATH}/minimal'
STARFISH_PATH = f'{DATA_PATH}/starfish.json'

# Data is tested in data_test.py
m = RobotData(f'{MIN_PATH}/min1.json')
s = RobotData(STARFISH_PATH)

# Robots tested in robot_test.py
minimal = Robot(m[0])
starfish = Robot(s[0])

m_tree = minimal.components
s_tree = starfish.components


class TestComponentsMinimal:

    def test_core(self):
        c = m_tree.get()[0]
        assert type(c[0]) == CoreComponent

    def test_hinge(self):
        c = m_tree.get()[1]
        assert type(c[0]) == ActiveHinge

    def test_brick(self):
        c = m_tree.get()[2]
        assert type(c[0]) == FixedBrick


class TestComponentsStarfish:

    def test_core(self):
        c = s_tree.get()[0]
        assert type(c[0]) == CoreComponent

    def test_hinge(self):
        c = s_tree.get()[1]
        assert type(c[0]) == ActiveHinge

    def test_brick(self):
        c = s_tree.get()[2]
        assert type(c[0]) == FixedBrick
