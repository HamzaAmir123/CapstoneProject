"""Common UI utilities"""

from enum import Enum

__author__ = "Jonty Doyle"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "21 September 2022"


class Mode(Enum):
    """Represents all modes at which the UI is in"""

    INTERACTIVE = 0
    COMMAND = 1
