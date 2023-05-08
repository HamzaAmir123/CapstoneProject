from ..util import RobotData
from ..robot import Robot

DATA_PATH = "data"
MIN_PATH = f'{DATA_PATH}/minimal'
STARFISH_PATH = f'{DATA_PATH}/starfish.json'

d = RobotData(STARFISH_PATH)
starfish = Robot(d[0])
s_tree = starfish.components


def test_hierarchy():
    # TODO: Validate hierarchy programmaticaly (currently validated visually)
    pass
