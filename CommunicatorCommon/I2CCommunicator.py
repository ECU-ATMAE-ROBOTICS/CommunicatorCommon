import logging
import asyncio

# Third Party
import smbus2


class I2CCommunicator:
    """
    A class to handle I2C communication.

    Attributes:
        busId (int): The I2C bus ID.
        address (int): The I2C device address.
    """

    logger = logging.getLogger(__name__)

    def __init__(self, busId: int, address: int) -> None:
        """
        Initialize the I2CCommunicator.

        Args:
            busId (int): The I2C bus ID.
            address (int): The I2C device address.
        """
        self._busId = busId
        self._address = address
        self._bus = smbus2.SMBus(busId)

    async def sendMsg(self, msg: bytes) -> None:
        """
        Send a message via I2C.

        Args:
            msg (bytes): The message to send.
        """
        self.logger.info("Sending data: %s", msg)
        try:
            await asyncio.to_thread(
                self._bus.write_i2c_block_data, self._address, 0, list(msg)
            )
        except Exception as e:
            self.logger.error("Error sending data: %s", str(e))

    async def receiveMsg(self, length: int) -> bytes:
        """
        Receive data of the specified length via I2C.

        Args:
            length (int): The length of the expected received data.

        Returns:
            bytes: The received data.
        """
        self.logger.info("Receiving data of length %d", length)
        try:
            receivedMsg = await asyncio.to_thread(
                self._bus.read_i2c_block_data, self._address, 0, length
            )
            return bytes(receivedMsg)
        except Exception as e:
            self.logger.error("Error receiving data: %s", str(e))
