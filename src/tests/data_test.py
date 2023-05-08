import pytest
from ..util import RobotData

DATA_PATH = "data"
MIN_PATH = f'{DATA_PATH}/minimal'
STARFISH_PATH = f'{DATA_PATH}/starfish.json'

single = RobotData(f'{MIN_PATH}/min1.json')
multiple = RobotData(f'{MIN_PATH}/multiple-minimal.json')

# TODO:
#   Test invalid JSON
#   Test if data is incorrect relative to Robogen Spec


class TestDataGeneral:

    def test_invalid_cs(self):
        with pytest.raises(SystemExit):
            RobotData('xyz')


class TestDataSingle:

    def test_id(self):
        id = single[0]["id"]
        assert id == 1

    def test_amount(self):
        body = single[0]["body"]
        assert len(body["part"]) == 5


class TestDataMutliple:

    def test_id(self):
        id = multiple[1]["id"]
        assert id == "id-2"

    def test_amount(self):
        body = multiple[1]["body"]
        assert len(body["part"]) == 5
