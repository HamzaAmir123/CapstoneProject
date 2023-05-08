"""Controls for manipulating RoboViz model camera"""

import math

# panda3d imports
from panda3d.core import Vec3

__author__ = "Jonty Doyle and Hamza Amir"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "21 September 2022"

# Constants for camera manipulation
ZOOM_INCREMENT = 15
ZOOM_MAX = 1500
ZOOM_MIN = 50
X_AXIS_INCREMENT = Vec3(1, 0, 0)
Y_AXIS_INCREMENT = Vec3(0, 1, 0)
MOVE_INCREMENT = 0.08
INIT_VIEW = Vec3(100, 100, 100)
DEFAULT_ORIGIN = Vec3(0, 0, 0)


class Camera:
    """Defines Camera for navigating through RoboViz model once rendered."""

    def __init__(self, base):
        self.base = base
        self.camera = self.base.camera
        self.currentOrigin = DEFAULT_ORIGIN
        self.currentView = INIT_VIEW
        self.__set_camera()

    def __set_camera(self):
        """Initialises camera defaults"""
        self.base.disableMouse()
        self.camera.setPos(INIT_VIEW)
        self.camera.lookAt(DEFAULT_ORIGIN)

    def __get_spherical(self):
        """Returns spherecial coordinates for a postion"""
        x, y, z = self.camera.getPos()
        return self.__cartesian_to_spherical(x, y, z)

    def __set_spherical(self, r, theta, phi):
        """Moves camera based on spherical coordinates"""
        new_pos = self.__spherical_to_cartesian(r, theta, phi)
        self.camera.setPos(new_pos)
        self.camera.lookAt(self.currentOrigin)

    def __cartesian_to_spherical(self, x, y, z):
        """Converts cartesian coordinates to spherical coordinates"""
        cx = self.currentOrigin[0]
        cy = self.currentOrigin[1]
        cz = self.currentOrigin[2]
        x = x - cx
        y = y - cy
        z = z - cz

        r = math.sqrt(x**2 + y**2 + z**2)
        theta = math.atan(math.sqrt(x**2 + y**2) / z)

        if x > 0:
            phi = math.atan(y / x)
        elif x < 0 and y >= 0:
            phi = math.atan(y / x) + math.pi
        elif x < 0 and y < 0:
            phi = math.atan(y / x) - math.pi
        elif x == 0 and y > 0:
            phi = math.pi / 2
        elif x == 0 and y > 0:
            phi = -math.pi / 2

        return r, theta, phi

    def __spherical_to_cartesian(self, r, theta, phi):
        """Converts spherical coordinates to cartesian coordinates"""
        cx = self.currentOrigin[0]
        cy = self.currentOrigin[1]
        cz = self.currentOrigin[2]
        x = r * math.cos(phi) * math.sin(theta) + cx
        y = r * math.sin(phi) * math.sin(theta) + cy
        z = r * math.cos(theta) + cz

        return x, y, z

    def zoom_in(self):
        """Defines zoom-in camera motion using spherical coordinates"""
        r, theta, phi = self.__get_spherical()

        if r > ZOOM_MIN:
            r -= ZOOM_INCREMENT
            self.__set_spherical(r, theta, phi)

    def zoom_out(self):
        """Defines zoom-out camera motion using spherical coordinates"""
        r, theta, phi = self.__get_spherical()

        if r < ZOOM_MAX:
            r += ZOOM_INCREMENT
            self.__set_spherical(r, theta, phi)

    def move_right(self):
        """Defines move right camera motion using spherical coordinates"""
        r, theta, phi = self.__get_spherical()
        phi += MOVE_INCREMENT
        self.__set_spherical(r, theta, phi)

    def move_left(self):
        """Defines move left camera motion using spherical coordinates"""
        r, theta, phi = self.__get_spherical()
        phi -= MOVE_INCREMENT
        self.__set_spherical(r, theta, phi)

    def move_up(self):
        """Defines move up camera motion using spherical coordinates"""
        r, theta, phi = self.__get_spherical()
        if theta > MOVE_INCREMENT:
            theta -= MOVE_INCREMENT
            self.__set_spherical(r, theta, phi)

    def move_down(self):
        """Defines move down camera motion using spherical coordinates"""
        r, theta, phi = self.__get_spherical()
        if theta < (math.pi / 2 - MOVE_INCREMENT):
            theta += MOVE_INCREMENT
            self.__set_spherical(r, theta, phi)

    def move_forward_xdir(self):
        """Defines move forward camera motion in x direction"""
        self.currentOrigin = self.currentOrigin + X_AXIS_INCREMENT
        self.currentView = self.currentView + X_AXIS_INCREMENT

        #self.camera.setPos(self.currentView)
        self.camera.lookAt(self.currentOrigin)

    def move_backward_xdir(self):
        """Defines move backward camera motion in x direction"""
        self.currentOrigin = self.currentOrigin - X_AXIS_INCREMENT
        self.currentView = self.currentView - X_AXIS_INCREMENT

        #self.camera.setPos(self.currentView)
        self.camera.lookAt(self.currentOrigin)

    def move_forward_ydir(self):
        """Defines move forward camera motion in y direction"""
        self.currentOrigin = self.currentOrigin + Y_AXIS_INCREMENT
        self.currentView = self.currentView + Y_AXIS_INCREMENT
        #self.camera.setPos(self.currentView)
        self.camera.lookAt(self.currentOrigin)

    def move_backward_ydir(self):
        """Defines move backward camera motion in y direction"""
        self.currentOrigin = self.currentOrigin - Y_AXIS_INCREMENT
        self.currentView = self.currentView - Y_AXIS_INCREMENT
        #self.camera.setPos(self.currentView)
        self.camera.lookAt(self.currentOrigin)

    def move_to_default_origin(self):
        """Returns camera to origin position"""
        self.currentOrigin = DEFAULT_ORIGIN
        self.camera.lookAt(self.currentOrigin)
