import time
import pickle
from pathlib import Path

# Relative imports
from ..robot import Robot, RobotData
from .parser import Parser
from .builder import RobotModel
from .terrain import Terrain
from .ui.common import Mode

__author__ = "Benjamin Chiddy and Jonty Doyle"
__email__ = "chdben002@myuct.ac.za"
__date__ = "21 September 2022"


class Environment:
    """Builds and renders either pre-loaded or custom robot models."""

    def __init__(self, base):
        self.base = base
        self.name = None
        self.console = base.ui.console
        self.robots = []
        self.ENV_DIR = base.DATA_DIR / 'environments'
        self.parser = Parser(self)
        self.logger = base.logger

        if not self.ENV_DIR.is_dir():
            self.ENV_DIR.mkdir()

    @property
    def envs(self):
        """Returns all saved environments"""
        envs = []
        try:
            for env in self.ENV_DIR.iterdir():
                envs.append(env.stem)
        except FileNotFoundError:
            return envs

        return envs

    @property
    def valid(self):
        """Defines test for checking whether input files are valid"""
        try:
            if self.config.valid and self.data.valid:
                return True
            else:
                return False
        except AttributeError:
            return False

    def clear(self, *args):
        """Removes all robots and terrain and closes resets environment.
        USAGE: clear
        """

        for robot in self.robots:
            robot.path.removeNode()

        self.robots = []
        self.name = None
        self.data = None
        self.config = None

        self.base.ui.refresh()
        try:
            self.terrain.path.removeNode()
        except AttributeError:
            return 'ERROR: No environment to clear.'

        return 'Environment Cleared'

    def save(self, *args):
        """Saves the current environment to disk as a Pickle file
        USAGE: save [name]
        """

        # State is represented as a 3-tuple of name, config & data
        if self.valid:
            try:
                self.name = args[0].strip("'").strip('"')
                file_name = f'{self.name}.pkl'
                state_path = self.ENV_DIR / file_name
                state = (self.name, self.data, self.config)
            except IndexError:
                if self.name is not None:
                    file_name = f'{self.name}.pkl'
                    state_path = self.ENV_DIR / file_name
                else:
                    return
        else:
            return 'ERROR: No data to save.'

        with state_path.open('wb+') as f:
            pickle.dump(state, f)

        self.base.ui.refresh()
        return f'"{self.name}" saved.'

    def unfocus(self, *args):
        """Dislay all robots
        USAGE: unfocus
        """

        for model in self.robots:
            model.path.show()

        return 'Unfocused'


    def focus(self, *args):
        """Focus a robot given an id.
        USAGE: focus [robot-id]
        """

        try:
            id = args[0]
        except IndexError:
            return None

        id_list = [r.robot.id for r in self.robots]

        if self.valid and id in id_list:
            for model in self.robots:
                model.path.hide()
                if model.robot.id == id:
                    model.path.show()

        else:
            return f'ERROR: id [{id}] not Found'

        return f'Viewing Robot {id}'

    def list(self, *args):
        """Lists all the saved environments.
        USAGE: list [name]
        """
        output = f'Environments: {", ".join(self.envs)}'
        return output

    def load(self, *args):
        """Loads an environment by name (searched in data directory).
        USAGE: load [name]
        """
        try:
            name = args[0]
            env = next((env for env in self.envs if env == name), None)
        except IndexError:
            return None

        if env is not None:
            path = self.ENV_DIR / f'{env}.pkl'

            with path.open('rb') as f:
                state = pickle.load(f)

            name, data, config = state

            self.clear()
            return self.__build(name, data, config)
        else:
            return f'Error: Environment "{name}" not found.'

    def open(self, *args):
        """Open a model given the configuration file parameters.
        USAGE: open [config-path] [position-path] [data-path]
        """
        try:
            self.config_path = Path(args[0])
            self.position_path = Path(args[1])
            self.data_path = Path(args[2])

            config = EnvironmentConfig(self.config_path)
            data = RobotData(self.data_path, self.position_path)

            return self.__build(None, data, config)
        except IndexError:
            return None

    def hide(self, *args):
        """Hides all rendered objects.
        USAGE: hide
        """
        try:
            for robot in self.robots:
                robot.path.hide()

            self.terrain.path.hide()

            return 'Environment Hidden'
        except AttributeError:
            return 'ERROR: No Environment to hide'

    def show(self, *args):
        """Show all rendered objects.
        USAGE: show
        """
        try:
            for robot in self.robots:
                robot.path.show()

            self.terrain.path.show()

            return 'Environment Visible'
        except AttributeError:
            return 'ERROR: No Environment to show'

    def rebuild(self, *args):
        """Rebuilds the environment under the current configuration
        USAGE: rebuild
        """
        try:
            self.clear()
            return self.open(self.config_path, self.position_path,
                             self.data_path)
        except AttributeError:
            return 'ERROR: Unable to detect filepaths to rebuild off.'

    def __build(self, name, data, config):
        """Private method which constructs/sets the environment given data
        and config"""
        self.base.ui.set_mode(Mode.INTERACTIVE)

        if data.valid and config.valid:
            self.data = data
            self.config = config
            self.name = name

            start_time = time.time()  # Start render timer.
            errors = 0
            # Add terrain
            self.terrain = Terrain(self.base, self.config)
            for i in range(self.config.num_robots):
                data, position = self.data[i]

                if position is None:
                    return f'ERROR: Position not-found/invalid [Robot ID: {i}]'
                elif data is None:
                    return f'ERROR: Data not found for Robot ID: {i}'
                else:
                    # Build robots
                    r = Robot(data, position)
                    errors += self.__add_robot(r)

                # Set Terrain & update lights
                self.base.lights.update(self.config)
                self.terrain.path.reparentTo(self.base.render)

            # End render timer.
            self.render_time = round(time.time() - start_time, 3)
            success = len(self.robots)

            added_text = f'Added {success} Robot(s) in {self.render_time}s'
            self.base.ui.set_mode(Mode.INTERACTIVE)
            self.base.ui.refresh()

            if errors > 0:
                error_text = f'{errors} Errors: View Log for Details'
                output = f'{added_text} [{error_text}]'
            else:
                output = added_text
            return output

        elif not data.valid:
            return 'Error: Invalid Robot .json File.'
        elif not config.valid:
            return 'Error: Invalid Environment Configuration'

    def __add_robot(self, robot: Robot):
        """Initialises a RobotBuilder to add a robot to the scene."""
        candidate = RobotModel(self.base, robot)
        id = candidate.id

        for robot in self.robots:
            if candidate.collides(robot):
                self.logger.error(f'Robot [id = {id}]: collision detected')
                return 1

        if not candidate.in_bounds(self.terrain):
            self.logger.error(f'Robot [id = {id}]: Out of Bounds')
            return 1
        else:
            self.logger.log(f'Added Robot [id = {id}]')
            candidate.path.reparentTo(self.base.render)
            self.robots.append(candidate)
            return 0


class EnvironmentConfig:
    """Holds attributes pertaining to the config spec provided"""

    def __init__(self, path):
        self.valid = True
        self.__parse_config(path)

    def __parse_config(self, path: Path):
        """Parses config txt file defining model to be rendered"""
        if path.is_file():
            with path.open('r') as f:
                data = f.read().split('\n')
                try:
                    self.x = float(data[0])
                    self.y = float(data[1])
                    self.num_robots = int(data[2])
                except (IndexError, ValueError):
                    self.valid = False
        else:
            self.valid = False
