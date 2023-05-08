__author__ = "Jonty Doyle"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "21 September 2022"


class Keybindings:
    """Defines keybindings for operating the camera to navigate
    through rendered model"""

    def __init__(self, base):
        self.base = base

        # Alias for easier reading
        camera = base.camera
        ui = base.ui
        environment = base.environment

        self.INTERACTIVE = {
            # Camera Bindings
            'control-j': camera.zoom_out,
            'control-k': camera.zoom_in,
            '-': camera.zoom_out,
            '=': camera.zoom_in,
            'k': camera.move_up,
            'j': camera.move_down,
            'h': camera.move_left,
            'l': camera.move_right,
            'arrow_up': camera.move_up,
            'arrow_down': camera.move_down,
            'arrow_left': camera.move_left,
            'arrow_right': camera.move_right,
            's': camera.move_backward_ydir,
            'w': camera.move_forward_ydir,
            'a': camera.move_backward_xdir,
            'd': camera.move_forward_xdir,
            'r': camera.move_to_default_origin,
            'shift-r': environment.rebuild,

            # UI & Environment
            'control-l': ui.console.clear,
            'shift-enter': ui.console.focus,
            'i': ui.console.focus,
            'q': ui.exit,
            'x': environment.clear,
        }

        self.COMMAND = {
            'escape': self.__handle_exit,
            'tab': ui.console.complete,
        }

        self.BINDINGS = [self.INTERACTIVE, self.COMMAND]

    def update(self):
        mode_bindings = self.BINDINGS[self.base.ui.mode.value]

        for bindings in self.BINDINGS:
            self.unset(bindings)

        self.set(mode_bindings)

    def set(self, bindings):
        """Initialises keybindings"""

        for key, event in bindings.items():
            self.base.accept(key, event)
            self.base.accept(f'{key}-repeat', event)

    def unset(self, bindings):
        """Unsets keybindings"""

        for key, event in bindings.items():
            self.base.ignore(key)
            self.base.ignore(f'{key}-repeat')

    def __handle_exit(self):
        ui = self.base.ui
        if ui.console.has_focus:
            ui.console.unfocus()
        else:
            ui.bar.unfocus()
