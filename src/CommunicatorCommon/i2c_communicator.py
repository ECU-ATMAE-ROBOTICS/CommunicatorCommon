"""Communicator for I2C Communication"""

import smbus2


class I2CCommunicator:
    """
    A class to handle I2C communication.

    Attributes:
        bus_id (int): The I2C bus ID.
    """

    def __init__(self, bus_id: int = 1) -> None:
        """
        Initialize the I2CCommunicator.

        Args:
            bus_id (int): The I2C bus ID. Default is 1.
        """
        self._bus_id = bus_id
        self._bus = smbus2.SMBus(bus_id)

    def send_msg(self, address: int, msg: bytes) -> None:
        """
        Send a message via I2C.

        Args:
            address (int): The I2C device address.
            msg (bytes): The message to send.

        Raises:
            Exception: If there is an I2C communication failure.
        """
        try:
            self._bus.write_i2c_block_data(address, 0, list(msg))
        except Exception as e:
            raise e

    def receive_msg(self, address: int, length: int) -> bytes:
        """
        Receive data of the specified length via I2C.

        Args:
            address (int): The I2C device address.
            length (int): The length of the expected received data.

        Returns:
            bytes: The received data.

        Raises:
            Exception: If there is an I2C communication failure.
        """
        try:
            received_msg = self._bus.read_i2c_block_data(address, 0, length)
            return bytes(received_msg)
        except Exception as e:
            raise e
