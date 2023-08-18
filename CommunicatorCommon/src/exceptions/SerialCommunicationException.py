class SerialCommunicationException(Exception):
    """Custom exception for serial communication errors."""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)
