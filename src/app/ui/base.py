"""This is the main menu screen for the RoboViz application. It is rendered
on start-up. DirectGUI is used to render all elements.

User can choose to create a custom model, load a saved model or exit to
desktop. Each selection renders another screen and hides this main menu.
"""
__author__ = "Benjamin Chiddy"
__email__ = "chdben002@myuct.ac.za"
__date__ = "28 August 2022"

import sys
from pathlib import Path

# GUI Rendering imports
from direct.gui.DirectFrame import DirectFrame

from .console import Console
from .common import Mode
from .bar import Bar
from ...util import Color


class BaseUI:
    """Main menu screen for RoboViz application"""

    def __init__(self, base):
        self.base = base
        self.mode = Mode.INTERACTIVE

        self.ASSET_DIR = Path(__file__).parents[3] / 'assets'

        # Colors
        self.COLORS = {
            'black': Color((0, 0, 0, 255)).value,
            'grey': Color((81, 97, 112, 255)).value,
            # 'bg-light': Color((216, 222, 233, 255)).value,
            'light-grey': Color((180, 180, 180, 255)).value,
            'grey-opaque': Color((81, 97, 112, 100)).value,
            'white': Color((229, 233, 240, 255)).value,
            'white-opaque': Color((229, 233, 240, 40)).value,

            'bg-dark': Color((59, 66, 82, 255)).value,
            'bg-opaque': Color((180, 180, 190, 170)).value,
            'bg-bar': Color((151, 97, 106, 240)).value,
            'bg-input': Color((59, 66, 82, 220)).value,

            # 'red': Color((208, 135, 112, 255)).value,
            'blue': Color((129, 161, 193, 255)).value,
            'red': Color((193, 76, 97, 240)).value,
            'none': Color((0, 0, 0, 0)).value
        }

        load_font = self.base.loader.loadFont
        # Fonts for menu system.
        FONT_PATH = self.ASSET_DIR / 'fonts'
        self.FONT_REGULAR = load_font(f'{FONT_PATH}/regular.ttf')
        self.FONT_ITALIC = load_font(f'{FONT_PATH}/italic.ttf')
        self.FONT_LIGHT = load_font(f'{FONT_PATH}/light.ttf')
        self.FONT_HEAVY = load_font(f'{FONT_PATH}/heavy.ttf')
        self.FONT_MONO = load_font(f'{FONT_PATH}/mono.ttf')
        self.FONT_MONO_ITALIC = load_font(f'{FONT_PATH}/mono-italic.ttf')

        # Container for main menu objects.
        self.frame = DirectFrame(frameColor=self.COLORS['none'],
                                 frameSize=(-1, 1, -1, 1),
                                 pos=(0, 0, 0),
                                 parent=self.base.aspect2d)

        self.console = Console(self)
        self.bar = Bar(self)

    def set_mode(self, mode: Mode):
        self.mode = mode

        self.base.bindings.update()

    def refresh(self):
        self.bar.refresh()

    def exit(self):
        """Exits application entirely"""
        sys.exit(0)
