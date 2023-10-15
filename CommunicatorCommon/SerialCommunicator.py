import asyncio
import serial
import logging
from typing import Optional

class SerialCommunicator:
    """
    A class for communicating through a serial port asynchronously.
    """

    def __init__(self, port: str= "dev/ttyACM0", baudRate: int=9600) -> None:
        """
        Initialize the SerialCommunicator class.

        Args:
            port (str): The name of the serial port to connect to.
            baudRate (int): The baud rate for the serial communication.
        """
        self._port = port
        self._baudRate = baudRate
        self._serialConnection = serial.Serial(port, baudRate)
        self._logger = logging.getLogger("SerialCommunicator")

    async def sendMessage(self, message: str) -> None:
        """
        Send a message through the serial port.

        Args:
            message (str): The message to be sent.
        """
        encodedMessage = message.encode()
        await asyncio.get_running_loop().run_in_executor(None, self._serialConnection.write, encodedMessage)
        self._logger.info(f"Sent message: {message}")

    async def receiveMessage(self, timeout: Optional[float] = None) -> str:
        """
        Receive a message from the serial port.

        Args:
            timeout (float, optional): Timeout in seconds for the operation.

        Returns:
            str: The received message.
        """
        receivedMessage = await asyncio.get_running_loop().run_in_executor(None, self._serialConnection.read)
        receivedMessage = receivedMessage.decode()
        self._logger.info(f"Received message: {receivedMessage}")
        return receivedMessage

    def close(self) -> None:
        """
        Close the serial connection.
        """
        self._serialConnection.close()
        self._logger.info("Serial connection closed.")