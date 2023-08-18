import logging
import asyncio
from typing import List

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
        self.eventQueue = asyncio.Queue()

        self.busId = busId
        self.address = address
        self.bus = smbus2.SMBus(busId)

    async def listenForEvents(self):
        """
        Listen for events and process them.
        """
        while True:
            event = await self.eventQueue.get()
            match event.eventType:
                case "send":
                    await self.sendMsg(event.data)
                case "receive":
                    await self.receiveMsg(event.data)
                case default:
                    return

    async def sendMsgEvent(self, msg: bytes):
        """
        Enqueue a send event with the provided message.

        Args:
            msg (bytes): The message to send.
        """
        await self.eventQueue.put(Event("send", msg))

    async def receiveMsgEvent(self, msgLength: int):
        """
        Enqueue a receive event with the provided message length.

        Args:
            msgLength (int): The length of the expected received message.
        """
        await self.eventQueue.put(Event("receive", msgLength))

    async def sendMsg(self, msg: bytes) -> None:
        """
        Send a message via I2C.

        Args:
            msg (bytes): The message to send.
        """
        self.logger.info("Sending data: %s", msg)
        try:
            await asyncio.to_thread(
                self.bus.write_i2c_block_data, self.address, 0, list(msg)
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
                self.bus.read_i2c_block_data, self.address, 0, length
            )
            return bytes(receivedMsg)
        except Exception as e:
            self.logger.error("Error receiving data: %s", str(e))
