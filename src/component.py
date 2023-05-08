"""Collection of classes which handle the creation of robot components"""

# Imports for model rendering
from pathlib import Path
from collections import defaultdict
from panda3d.core import Material

# Helps with component colouring.
from .util import Color

__author__ = "Jonty Doyle and Hamza Amir"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "21 September 2022"

BASE_DIR = Path(__file__).parents[1]
COMPONENT_DIR = BASE_DIR / 'assets' / 'models' / 'components' / 'egg'


class ComponentTree:
    """
    An N-Ary tree of component objects (specifically their subclasses).
    Constructs the tree, and stores attributes pertaining to the tree itself.

    Parameters
    ---------
    component_list: List -- A list of Component Subclasses
    """

    def __init__(self, component_list):
        self.components = component_list
        self.root = self.__get_root(self.components)
        self.size = len(self.components)

    def __get_root(self, components):
        """Returns root Component of tree."""
        for _, component in components.items():
            if component.root:
                return component
        return None

    def __get(self, node, list, parent=None, slot=None):
        """Returns all child components of a specified parent as a list.
        Searches recursively appending a list at each tree level."""
        data = (node, parent, slot)
        list.append(data)

        for slot, child in node.children.items():
            self.__get(child, list, node, slot)
        return list

    def get(self):
        """Public accesor for get method.
        Returns all child components of a specified parent as a list."""
        list = []
        return self.__get(self.root, list)

    def find_node(self, node, id):
        """Returns a specified component by searching tree recursively."""
        if node.id == id:
            return node

        for _, child in node.children.items():
            return_node = self.find_node(child, id)
            if return_node:
                return return_node

        return None

    def print(self, node, slot=0, output=[], level=0):
        """Prints component tree structure to terminal.
        Tree levels are represented by indents."""
        output.append(f'{"  "*level} {slot} {str(node)} ({node.orientation})')
        level += 1
        for slot, child in node.children.items():
            self.print(child, slot, output, level)

        return '\n'.join(output)

    def __repr__(self):
        """Returns string representation of a component tree."""
        return self.print(self.root)


class Component:
    """
    The base class representing a component.
    Stores key attributes pertaining to the construction/rendering
    of each component model, as well as a dictionary of Components,
    serving as children in the tree.

    Parameters
    ---------
    data: dict -- A dictionary of Robogen compatible data (parsed from JSON)
    """

    def __init__(self, data: dict):
        self.id = data['id']
        self.root = data['root']
        self.orientation = data['orientation'] * 90
        self.children = defaultdict(None)  # List of children.
        self.model_path = f'{COMPONENT_DIR}/{type(self).__name__}'  # Location of egg files.
        self.model_size = None  # Set during build

    @property
    def slots_in(self):
        """Checks if component slots into another component"""
        name = type(self).__name__

        if 'Hinge' in name:
            return True
        elif 'Sensor' in name:
            return True
        elif 'Wheel' in name:
            return True
        else:
            return False

    @property
    def has_slot(self):
        """Checks if component has a connection slot"""
        name = type(self).__name__

        if 'FixedBrick' in name:
            return True
        elif 'CoreComponent' in name:
            return True
        else:
            return False

    @property
    def is_terminal(self):
        """Checks if component is a terminal component"""
        try:
            return self.TERMINAL
        except AttributeError:
            return False

    @property
    def is_one_way(self):
        """Checks if component is a one-way component"""
        name = type(self).__name__
        if 'Hinge' in name:
            return True
        elif 'Sensor' in name:
            return True
        elif 'Wheel' in name:
            return True
        else:
            return False

    def get_material(self, robot):
        """Returns specifics for component rendering in panda3d model."""
        c = Color(self.color)
        m = Material()  # Class which handles rendering in panda3d

        m.setShininess(8)
        m.setRefractiveIndex(0.8)
        m.setDiffuse(c.darken(0.9))
        m.setEmission(c.darken(0.6))
        m.setSpecular(c.lighten(1.2))

        return m

    def set_pos(self, x, y):
        """Sets x, y positions of a robot"""
        self.x = x
        self.y = y

    def __repr__(self):
        """Returns string representation of Component"""
        return f'{self.id}: {type(self).__name__}'

    def __str__(self):
        """Returns string representation of Component"""
        return f'{self.id}: {type(self).__name__}'


# -- Bricks


class CoreComponent(Component):
    """Defines the CoreComponent type component (root).
    Inherits from Component class.

    Parameters
    ---------
    robot: Robot -- The robot to which it is a member of.
    """

    def __init__(self, data, robot):
        super().__init__(data)
        self.color = (50, 168, 68, 100)  # Sets core colour to green
        self.material = super().get_material(robot)


class FixedBrick(Component):
    """Defines Fixed Brick type component.
    Inherits from Component class.

    Parameters
    ---------
    robot: Robot -- The robot to which it is a member of.
    """

    def __init__(self, data, robot):
        super().__init__(data)
        self.color = (168, 60, 50, 100)  # Sets FixedBrick to red
        self.material = super().get_material(robot)


# -- Hinges


class ActiveHinge(Component):
    """Defines Active Hinge type component.
    Inherits from Component class.

    Parameters
    ---------
    robot: Robot -- The robot to which it is a member of.
    """

    def __init__(self, data, robot):
        super().__init__(data)
        self.color = (89, 20, 66, 0)  #Sets ActiveHinge to brown
        self.material = super().get_material(robot)


class PassiveHinge(Component):
    """Defines Passive Hinge type component.
    Inherits from Component class.

    Parameters
    ---------
    robot: Robot -- The robot to which it is a member of.
    """

    def __init__(self, data, robot):
        super().__init__(data)
        self.color = (112, 28, 186, 100)  # Sets PassiveHinge to purple
        self.material = super().get_material(robot)


# -- Wheels


class ActiveWheel(Component):
    """Defines Active Rotation Wheel type component.
    Inherits from Component class.

    Parameters
    ---------
    robot: Robot -- The robot to which it is a member of.
    """

    def __init__(self, data, robot):
        super().__init__(data)
        self.color = (46, 62, 184, 100)  # Sets ActiveWheel to blue
        self.material = super().get_material(robot)
        self.TERMINAL = True


class PassiveWheel(Component):
    """Defines Passive Rotation Wheel type component.
    Inherits from Component class.

    Parameters
    ---------
    robot: Robot -- The robot to which it is a member of.
    """

    def __init__(self, data, robot):
        super().__init__(data)
        self.color = (255, 128, 0, 0)  # Sets PassiveWheel to orange
        self.material = super().get_material(robot)
        self.TERMINAL = True


# -- Sensors


class IrSensor(Component):
    """Defines Ir Sensor type component.
    Inherits from Component class.

    Parameters
    ---------
    robot: Robot -- The robot to which it is a member of.
    """

    def __init__(self, data, robot):
        super().__init__(data)
        self.color = (255, 215, 0, 0)  # Sets to yellow
        self.material = super().get_material(robot)
        self.TERMINAL = True


class TouchSensor(Component):
    """Defines Touch Sensor type component.
    Inherits from Component class.

    Parameters
    ---------
    robot: Robot -- The robot to which it is a member of.
    """

    def __init__(self, data, robot):
        super().__init__(data)
        self.color = (112, 28, 186, 100)  # Sets to purple
        self.material = super().get_material(robot)
        self.TERMINAL = True


class LightSensor(Component):
    """Defines Passive Hinge type component.
    Inherits from Component class.

    Parameters
    ---------
    robot: Robot -- The robot to which it is a member of.
    """

    def __init__(self, data, robot):
        super().__init__(data)
        self.color = (112, 28, 186, 100)  # Sets to purple
        self.material = self.__get_material(robot)
        self.TERMINAL = True
