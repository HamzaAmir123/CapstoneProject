import pytest
from ..util import RobotData
from ..robot import Robot
from ..component import ComponentTree

DATA_PATH = "data"
MIN_PATH = f'{DATA_PATH}/minimal'
STARFISH_PATH = f'{DATA_PATH}/starfish.json'

# Data is tested in data_test.py
m = RobotData(f'{MIN_PATH}/min1.json')
s = RobotData(STARFISH_PATH)

minimal = Robot(m[0])
starfish = Robot(s[0])


class TestRobotGeneral:

    def test_invalid_cs(self):
        with pytest.raises(SystemExit):
            Robot('xyz')

class TestRobotMinimal:

    def test_id(self):
        data_id = m[0]["id"]
        assert minimal.id == str(data_id)

    # Tests if the number of components match the data
    def test_num_components(self):
        num_components = len(m[0]["body"]["part"])
        assert len(minimal.components.get()) == num_components

    # Type assertation
    def test_components(self):
        assert type(minimal.components) == ComponentTree


class TestRobotStarfish:

    def test_id(self):
        data_id = s[0]["id"]
        assert starfish.id == str(data_id)

    # Tests if the number of components match the data
    def test_num_components(self):
        num_components = len(s[0]["body"]["part"])
        assert len(starfish.components.get()) == num_components

    # Type assertation
    def test_components_type(self):
        assert type(starfish.components) == ComponentTree
