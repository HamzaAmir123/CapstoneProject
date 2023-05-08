"""Utils class for error handling and colour handling within models"""

import sys

__author__ = "Jonty Doyle & Hamza Amir"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "21 September 2022"


def print_err(string):
    """Helper function to print and exit"""
    print(string)
    sys.exit(1)


class Color:
    """
    Helper Class to manipulate RGBA colors.
    Uses American spelling (sorry)

    Parameters
    ----------
    rgba: 4-Tuple -- (R,G,B,A)
    """

    def __init__(self, rgba):
        self.color = tuple([x / 255 for x in rgba])

    @property
    def value(self):
        """Returns RGBA value for a color"""
        return self.color

    def darken(self, value):
        """Darkens RGBA shade"""
        r, g, b, a = self.color
        output = [round(x * (1 - value), 3) for x in (r, g, b)]
        output.append(a)

        return tuple(output)

    def lighten(self, value):
        """Lightens RGBA shade"""
        r, g, b, a = self.color
        output = [round(x * (1 + value), 3) for x in (r, g, b)]
        output.append(a)

        return tuple(output)
