"""This is a console object rendered across the bottom of a render which
displays import model interaction information with user"""

# panda3d import
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectFrame import DirectFrame
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

from ..logger import Logger
from .common import Mode

__author__ = "Jonty Doyle"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "21 September 2022"

# Initial text to be displayed
START_TEXT = "Welcome to RoboViz! Press i to open console and use [help] to get started."
END_TEXT = "Press h for help"


class Console:
    """Console object for displaying model messages to user.
    Rendered across bottom of application screen"""

    def __init__(self, base):
        self.app = base.base
        self.base = base

        self.frame = DirectFrame(frameColor=base.COLORS['bg-opaque'],
                                 frameSize=(-5, 5, 0.08, 0),
                                 pos=(0, 0, 0),
                                 parent=base.base.a2dBottomLeft)

        self.input = DirectEntry(initialText='',
                                 parent=self.frame,
                                 frameSize=(-100, 100, 1.2, 0),
                                 frameColor=base.COLORS['bg-dark'],
                                 pos=(0.06, 0, 0.02),
                                 text_fg=base.COLORS['white'],
                                 scale=0.05,
                                 width=110,
                                 numLines=1,
                                 entryFont=base.FONT_MONO,
                                 command=self.parse)

        self.output = OnscreenText(text=START_TEXT,
                                   parent=self.frame,
                                   fg=base.COLORS['bg-dark'],
                                   pos=(0.02, 0.02),
                                   scale=.05,
                                   align=TextNode.ALeft,
                                   font=base.FONT_MONO_ITALIC)

        self.indicator = OnscreenText(text='>',
                                      parent=self.frame,
                                      fg=base.COLORS['blue'],
                                      pos=(0.02, 0.02),
                                      scale=.05,
                                      align=TextNode.ALeft,
                                      font=base.FONT_MONO)
        self.logger = self.app.logger
        self.input.hide()
        self.indicator.hide()

    @property
    def has_focus(self):
        return self.input['focus']

    def print(self, text, error=False):
        """Prints message to console given text."""
        if error:
            self.output['fg'] = self.base.COLORS['red']
        else:
            self.output['fg'] = self.base.COLORS['bg-dark']

        self.input.set('')
        self.input.hide()
        self.output.setText(text)
        self.output.show()

    def log(self, text):
        """Logs a message to RoboViz Logger."""
        self.indicator.hide()
        self.print(text)
        self.input.set('')
        self.logger.log(text)

    def clear(self):
        """Clears console"""
        self.output.setText('')

    def focus(self):
        self.frame['frameColor'] = self.base.COLORS['bg-dark']
        self.input['focus'] = True
        self.input.show()
        self.indicator.show()
        self.input.set('')
        self.output.setText('')
        self.output.hide()
        self.base.set_mode(Mode.COMMAND)

    def unfocus(self):
        self.frame['frameColor'] = self.base.COLORS['bg-opaque']
        self.input['focus'] = False
        self.indicator.hide()
        self.input.set('')
        self.input.hide()
        self.output.show()
        self.base.set_mode(Mode.INTERACTIVE)

    def parse(self, text):
        parser = self.app.environment.parser
        if text != '':
            output, return_value = parser.parse(text)

            if return_value == 1:
                self.print(output, error=True)
            else:
                self.print(output)
        self.unfocus()

    def complete(self):
        parser = self.app.environment.parser
        input = self.input.get()

        text = parser.complete(input)

        self.input.set(f'{text}')
        self.input.setCursorPosition(len(text))
