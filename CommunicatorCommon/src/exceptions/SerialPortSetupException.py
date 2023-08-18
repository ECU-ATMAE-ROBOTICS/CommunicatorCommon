# Internal
from .SerialCommunicationException import SerialCommunicationException


class SerialPortSetupException(SerialCommunicationException):
    """Exception for errors during serial port setup."""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)
