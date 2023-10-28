# Third Party
import smbus2


class I2CCommunicator:
    """
    A class to handle I2C communication.

    Attributes:
        busId (int): The I2C bus ID.
    """

    def __init__(self, busId: int = 1) -> None:
        """
        Initialize the I2CCommunicator.

        Args:
            busId (int): The I2C bus ID.
            address (int): The I2C device address.
        """
        self._busId = busId
        self._bus = smbus2.SMBus(busId)

    def sendMsg(self, address: int, msg: bytes) -> None:
        """
        Send a message via I2C.

        Args:
            msg (bytes): The message to send.
        """
        try:
            self._bus.write_i2c_block_data(address, 0, list(msg))
        except Exception as e:
            raise e

    def receiveMsg(self, address: int, length: int) -> bytes:
        """
        Receive data of the specified length via I2C.

        Args:
            length (int): The length of the expected received data.

        Returns:
            bytes: The received data.
        """
        try:
            receivedMsg = self._bus.read_i2c_block_data(address, 0, length)
            return bytes(receivedMsg)
        except Exception as e:
            raise e
