from .SerialCommunicationError import SerialCommunicationError


class SerialPortSetupError(SerialCommunicationError):
    """Exception for errors during serial port setup."""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)
