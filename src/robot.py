"""Collection of classes which handle the creation of Robots"""

from pathlib import Path
import importlib
import random
import json
from json import JSONDecodeError

# panda3d imports
from panda3d.core import Vec3
from .component import ComponentTree

# Utils for robot customisation
from .util import Color, print_err
# Component imports to assit in building robots

__author__ = "Jonty Doyle & Hamza Amir"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "21 September 2022"


class Robot:
    """
    Represents logical abstraction of a robot in the
    RoboViz application.
    Made up of components defined in Components (subclasses)

    Refer to:
    https://docs.python.org/3/library/json.html#json-to-py-table

    Parameters
    ---------
    data: dict -- A dict of JSON decoded data, specified by Robogen
    position: tuple -- A tuple resembling its x,y point in the environment.
    """

    def __init__(self, data, position):
        try:
            self.id = str(data['id'])
            self.color = self.__pick_color()
            self.brain = data['brain']
            self.components = self.__build_tree(data['body'])
            self.position = position
        except TypeError:
            print_err(f'Incorrect data passed to Robot constructor: {data}')

    def __build_tree(self, data):
        """Returns a tree rooted at the CoreComponent based on input JSON"""

        component_module = importlib.import_module('.component', package='src')
        components = {}
        for component in data['part']:
            try:
                ComponentType = getattr(component_module, component['type'])
                c = ComponentType(component, self)
                components[c.id] = c
            except AttributeError:
                pass

        for id, component in components.items():
            for connection in data['connection']:
                src = connection["src"]
                dest = connection["dest"]
                slot = connection["srcSlot"]

                if id == src:
                    try:
                        component.children[slot] = components[dest]
                    except KeyError:
                        print(f'No connection found for {src} -> {dest}')

        return ComponentTree(components)

    def __pick_color(self):
        """Randomly picks a color attribute to pass to components."""
        COLORS = {
            'Blue': (46, 62, 184, 100),
            'Green': (50, 168, 68, 100),
            'Red': (168, 60, 50, 100),
            'Orange': (245, 129, 47, 100),
            'Purple': (112, 28, 186, 100),
        }

        options = list(COLORS.values())
        choice = random.choice(options)
        return Color(choice)

    def __repr__(self):
        """Returns string representation of a robot"""
        return f'id: {self.id} \nparts: {self.components}'


class RobotData:
    """
    Parses, stores and retrieves Robot data required for constructing a
    robot - critical to represent the state of the Environment.

    Parameters
    ---------
    data_path: Path -- Path to data (.json) file.
    position_path: Path -- Path to position file.
    """

    def __init__(self, data_path: Path, position_path: Path):
        self.valid = True
        self.data_path = data_path
        self.position_path = position_path
        self.__robot_data = self.__load_data(data_path)
        self.__position_data = self.__load_positions(position_path)

    @property
    def heterogenous(self):
        """Checks if model to be rendered is a swarm as defined in JSON file"""
        if 'swarm' not in self.__robot_data:
            return True
        else:
            return False

    def __load_positions(self, path):
        """Parses robots positions based on positions txt file"""
        positions = []
        if path.is_file():
            with path.open('r') as f:
                data = f.read().split('\n')
        else:
            return None

        for position in data:
            try:
                if len(position) != 0:
                    x, y, z = tuple(position.split(' '))
                    positions.append(Vec3(int(x), int(y), int(z)))
            except ValueError:
                pass

        return positions

    def __load_data(self, path):
        """Parses robot data from inputted JSON file"""
        if path.is_file():
            with open(path) as f:
                try:
                    data = json.load(f)
                except JSONDecodeError:
                    self.valid = False
                    return None
        else:
            self.valid = False
            return None

        return data

    def __getitem__(self, value):
        """Returns robot and its position from parsed inputs for rendering"""
        if self.valid:
            try:
                position = self.__position_data[value]
            except IndexError:
                position = None

        if self.heterogenous:
            data = self.__robot_data
        else:
            try:
                data = self.__robot_data['swarm'][value]
            except IndexError:
                length = len(self.__robot_data['swarm'])
                data = self.__robot_data['swarm'][value % length]

        return data, position
