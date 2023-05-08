"""Collection of classes which log specific errors that happen during runtime.
Used extensively to test model is operating correctly"""

from enum import Enum
from pathlib import Path

from ..util import print_err

__author__ = "Jonty Doyle"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "21 September 2022"


class Severity(Enum):
    """Enum specifying the severity of an error that occured"""
    INFO = 0
    ERROR = 1


class Logger:
    """Defines interactions"""

    def __init__(self, data_path: Path):
        self.history = []
        self.path = data_path / 'roboviz.log'

    def log(self, text):
        """Adds message to log history"""
        message = LogMessage(text, Severity.INFO)
        self.history.append(message)

    def error(self, text):
        """Adds error to log history"""
        message = LogMessage(text, Severity.ERROR)
        self.history.append(message)

    def clear(self):
        """Clears current log history"""
        self.history = []

    def write(self):
        """Writes message to log file"""
        with self.path.open('w') as f:
            for message in self.history:
                f.write(str(message))


class LogMessage:
    """Defines log messages which are wrriten to log file found in root dir."""

    def __init__(self, text, severity: Severity):
        self.text = text  # Message body
        self.severity = severity  # Error severity

    @property
    def is_error(self):
        """Checks if log message is an error message"""
        if self.severity == Severity.ERROR:
            return True
        else:
            return False

    def __str__(self):
        """Returns string representation of log message"""
        return f'{self.severity.name}, {self.text}\n'
