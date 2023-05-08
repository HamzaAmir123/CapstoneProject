"""This is a pop-up menu that appears when a user decides to create a custom
model on the main menu. DirectGUI is used to render all elements.

Default parameters are set to the starfish model. User can change these but
must ensure files are in the /config folder.
"""
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectDialog import OkCancelDialog
from direct.gui.DirectGui import DGG

__author__ = "Benjamin Chiddy"
__email__ = "chdben002@myuct.ac.za"
__date__ = "21 September 2022"


class Create:
    """Create custom model pop-up menu for RoboViz application"""

    def __init__(self, base):
        self.base = base
        self.app = base.base
        self.NUM_INPUTS = 3

        # Stores references to the text input (default below)
        self.paths = [
            "config/single/config.txt",
            "config/single/positions.txt",
            "data/starfish.json"
        ]

        # Dialog box for pop-up menu. Uses itemSel for button logic.

        self.dialog = OkCancelDialog(dialogName="createModelFrame",
                                     parent=self.base.frame,
                                     command=self.select,
                                     sidePad=0.6,
                                     topPad=0.7,
                                     relief=DGG.FLAT,
                                     buttonTextList=["Build", "Cancel"],
                                     buttonValueList=[True, False],
                                     pos=(0, -0.2, -0.2))

        # Pop-up title text.
        self.title = OnscreenText(text="Enter model parameters:",
                                  parent=self.dialog,
                                  pos=(0, 0.6, 0.6),
                                  scale=.06,
                                  font=base.FONT_LIGHT)

        self.text_boxes = self.__build_text_boxes()
        self.input_boxes = self.__build_input_boxes()

    def __build_input_boxes(self):
        """Builds all specified input boxes given kwargs"""

        input_boxes = []
        for i in range(self.NUM_INPUTS):
            input_kwargs = self.__get_input_kwargs(i, self.paths[i])
            input = DirectEntry(**input_kwargs)
            input_boxes.append(input)

        return input_boxes

    def __build_text_boxes(self):
        """Builds all specified text boxes given kwargs"""

        text = ['Config Path:', 'Position Path:', 'Robot Path:']
        text_boxes = []

        for i in range(self.NUM_INPUTS):
            text_kwargs = self.__get_text_kwargs(i, text[i])
            text_box = OnscreenText(**text_kwargs)
            text_boxes.append(text_box)

        return text_boxes

    def __get_text_kwargs(self, number, text):
        """Generates keyword arguments handed to OnscreenText"""

        pos = self.__get_height(number)
        return {
            'text': text,
            'scale': 0.06,
            'parent': self.dialog,
            'pos': (-0.63, pos, pos),
            'font': self.base.FONT_LIGHT,
        }

    def __get_input_kwargs(self, number, text):
        """Generates keyword arguments handed to DirectEntry"""

        pos = self.__get_height(number)
        return {
            'scale': 0.06,
            'width': 20.5,
            'initialText': text,
            'numLines': 1,
            'parent': self.dialog,
            'pos': (-0.4, pos, pos),
            'frameColor': (142, 250, 250, 1),
            'focusOutCommand': self.__fetch_paths,
            'entryFont': self.base.FONT_LIGHT,
        }

    def __get_height(self, i):
        """Handles input & text box height"""
        return 0.05 + 0.2 * i

    def __fetch_paths(self):
        """Called to fetch paths from input box prior to building"""
        for i, input in enumerate(self.input_boxes):
            self.paths[i] = input.get()

    def select(self, create):
        """Logic for dialog box. User can either Build model based
        on speficied parameters or cancel and close creation menu."""

        self.__fetch_paths()
        config, position, data = self.paths

        # Create Button is Clicked
        if create:
            self.app.environment.clear()
            # Renders model if files are valid.
            console = self.base.console
            console.print(self.app.environment.open(config, position, data))

        # Cleans & exits dialogue
        self.dialog.cleanup()
        self.base.exit_dialogue()
