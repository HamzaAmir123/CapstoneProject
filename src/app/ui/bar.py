from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectEntry import DirectEntry
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from pathlib import Path

from .create import Create
from .common import Mode

__author__ = "Jonty Doyle"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "21 September 2022"


class Bar:

    def __init__(self, base):
        self.base = base
        self.app = base.base
        IMAGE_PATH = self.base.ASSET_DIR / 'images'
        BUTTON_SIZE = (-0.7, 0.7, -0.7, 0.7)
        BUTTON_SCALE = 0.04
        MENU_HEIGHT = 0.14
        BAR_HEIGHT = -MENU_HEIGHT
        self.DEFAULT_NAME = 'Untitled Environment'

        # self.__bg = DirectFrame(frameColor=base.COLORS['bg-bar'],
        #                         frameSize=(0.03, 0.58, -0.13, -0.135),
        #                         pos=(0, 0, 0),
        #                         parent=self.app.a2dTopLeft)

        self.save_entry = DirectEntry(parent=self.app.a2dTopLeft,
                                      frameSize=(-1.4, 11, -0.5, 1.3),
                                      frameColor=base.COLORS['bg-opaque'],
                                      pos=(0.10, 1, -0.1),
                                      text_fg=base.COLORS['bg-dark'],
                                      scale=0.05,
                                      width=110,
                                      numLines=1,
                                      entryFont=base.FONT_MONO_ITALIC,
                                      command=self.__exec_save,
                                      focusInCommand=self.__focus_save,
                                      focusOutCommand=self.__unfocus_save)

        self.__caret = OnscreenText(text=">",
                                    parent=self.app.a2dTopLeft,
                                    pos=(0.07, -0.1),
                                    scale=0.05,
                                    font=self.base.FONT_MONO,
                                    fg=self.base.COLORS['red']
                                    )

    def unfocus(self):
        """Show all items in the bar"""
        self.save_entry['focus'] = False

    def load_menu(self):
        """Switchs to the model menu screen."""
        pass

    def __focus_save(self):
        """Switchs to the model menu screen."""
        entry = self.save_entry
        length = len(entry.get())
        entry.setCursorPosition(length)

        # entry['fg'] = self.base.COLORS['']
        entry['frameColor'] = self.base.COLORS['white']
        self.base.set_mode(Mode.COMMAND)
        if entry.get() == self.DEFAULT_NAME:
            entry.set('')

    def __unfocus_save(self):
        """Switchs to the model menu screen."""
        entry = self.save_entry
        entry['frameColor'] = self.base.COLORS['bg-opaque']
        text = entry.get()

        try:
            name = self.app.environment.name
            if name != text:
                entry.set(self.DEFAULT_NAME)
        except AttributeError:
            entry.set(self.DEFAULT_NAME)

        self.base.set_mode(Mode.INTERACTIVE)

    def __exec_save(self, text):
        """Switchs to the model menu screen."""
        if text != '':
            self.base.console.parse(f'save {text}')

    def refresh(self):
        try:
            name = self.app.environment.name
            if name is None:
                text = self.DEFAULT_NAME
            else:
                text = name

        except AttributeError:
            text = self.DEFAULT_NAME

        self.save_entry.set(text)

    def clear(self):
        self.base.console.log(self.app.environment.clear())
