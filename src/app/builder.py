"""Handles building robots and placing them in the model environment."""

from pathlib import Path

# Imports to handle robot building
from ..robot import Robot
from .terrain import Terrain
from panda3d.core import NodePath

__author__ = "Jonty Doyle and Hamza Amir"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "21 September 2022"

BASE_DIR = Path(__file__).parents[2]
COMPONENT_DIR = BASE_DIR / 'assets' / 'models' / 'components' / 'egg'
TOLERANCE = 0.02  # Offset for slotting two components together
SLOT_OFFSET = 0.15 + TOLERANCE  # Offset for slotting two components together

# Constants used in robot building
SCALE = 0.1


class RobotModel:
    """
    Responsible for the construction/render of a single robot, further
    provides public methods for checking collisions and determining if two
    components slot in together.

    Parameters
    ---------
    base: ShowBase -- A reference to the application root.
    robot: Robot -- The robot to be rendered.
    """

    def __init__(self, base, robot: Robot):
        self.base = base
        self.robot = robot

        self.path = self.__build_path(robot, robot.position)
        self.bounds = self.path.getTightBounds()
        self.position = robot.position
        self.id = robot.id

    def collides(self, other):
        """Checks if candidate robot will collide with an already
        rendered robot. Returns True if they overlap False if not"""

        o_start, o_end = other.bounds
        o_x = (o_start.x, o_end.x)  # x-bounds for other robot
        o_y = (o_start.y, o_end.y)  # y-bounds for other robot

        r_start, r_end = self.bounds
        r_x = (r_start.x, r_end.x)  # x-bounds for robot
        r_y = (r_start.y, r_end.y)  # y-bounds for robot

        if self.__overlap(r_x, o_x) and self.__overlap(r_y, o_y):
            return True

        return False

    def in_bounds(self, terrain: Terrain):
        """Checks whether candidate robot will be rendered within the defined
        terrain"""
        start, end = self.bounds
        _, terrain_bounds = terrain.bounds
        x, y, _ = terrain_bounds

        if (-x < start.x < x) and (-x < end.x < x):
            if (-y < start.y < y) and (-y < end.y < y):
                return True

        return False

    def __overlap(self, point1, point2):
        """Checks whether the bounding box of two robots will overlap.
        Returns True if overlap is going to occur, False if not."""
        if (point1[1] >= point2[0] and point2[1] >= point1[0]):
            return True
        else:
            return False

    # Returns the orientation according to:
    # https://robogen.org/docs/building-your-robot/#3D-print
    def __find_orientation(self, slot):
        """Returns the orientation according to:
        https://robogen.org/docs/building-your-robot/#3D-print"""
        if slot == 0:
            return 90
        elif slot == 1:
            return 270
        elif slot == 2:
            return 0
        elif slot == 3:
            return 180

    def __build_path(self, robot: Robot, position):
        """Sets node path for robot to be rendered into scene graph"""
        node = NodePath(robot.id)
        for component in robot.components.get():
            self.__add_component(component, node)

        size = self.__get_size(node)

        node.setPos(position)
        node.setZ(size.z / 2)
        return node

    def __add_component(self, data, path):
        """Base function for adding a component to the scene graph"""
        component, parent, slot = data
        component_path = NodePath(component.id)
        model_path = self.__fetch_model(component, parent, slot)
        model_path.reparentTo(component_path)

        root = self.robot.components.root

        if component != root:
            slot_path = self.__build_slot(component, parent, slot)
            parent_path = path.find(f'**/{parent.id}*')
            slot_path.reparentTo(parent_path)
            self.__place_component(component, parent, component_path)
            component_path.reparentTo(slot_path)
        else:
            component_path.reparentTo(path)

    def __fetch_model(self, component, parent, slot):
        """Fetches the component (egg) model, rotates accordingly"""
        model = self.base.loader.loadModel(component.model_path)

        model.setScale(SCALE)
        model.setMaterial(component.material)
        component.model_size = self.__get_size(model)

        # Rotate only if not always in one direction
        if not component.is_one_way:
            model.setH(component.orientation)

        return model

    def __build_slot(self, component, parent, slot):
        """Creates the slot and rotates accordingly"""
        slot_path = NodePath(str(slot))

        if parent.is_one_way:
            slot_path.setH(self.__find_orientation(2))  # Only One slot
        else:
            slot_path.setH(self.__find_orientation(slot) + parent.orientation)

        return slot_path

    def __place_component(self, component, parent, path):
        """Places the component by setting the distance from slot (parent)"""
        size_difference = (parent.model_size.x - component.model_size.x) / 2 - TOLERANCE

        if parent.has_slot and component.slots_in:
            path.setX(parent.model_size.x - size_difference - SLOT_OFFSET)
        elif parent.slots_in and component.has_slot:
            path.setX(parent.model_size.x - size_difference - SLOT_OFFSET)
        else:
            path.setX(parent.model_size.x - size_difference)

        return path

    def __get_size(self, model):
        """Helper for finding the size of a model"""
        min, max = model.getTightBounds()
        size = max - min
        return size
