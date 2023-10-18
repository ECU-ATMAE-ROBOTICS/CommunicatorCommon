import asyncio
import serial
from typing import Optional


class SerialCommunicator:
    """
    A class for communicating through a serial port asynchronously.
    """

    def __init__(self, port: str = "dev/ttyACM0", baudRate: int = 9600) -> None:
        """
        Initialize the SerialCommunicator class.

        Args:
            port (str): The name of the serial port to connect to.
            baudRate (int): The baud rate for the serial communication.
        """
        self._port = port
        self._baudRate = baudRate
        self._serialConnection = serial.Serial(port, baudRate)

    async def sendMessage(self, message: str) -> None:
        """
        Send a message through the serial port.

        Args:
            message (str): The message to be sent.
        """
        encodedMessage = message.encode()
        await asyncio.get_running_loop().run_in_executor(
            None, self._serialConnection.write, encodedMessage
        )

    async def receiveMessage(self, timeout: Optional[float] = None) -> str:
        """
        Receive a message from the serial port.

        Args:
            timeout (float, optional): Timeout in seconds for the operation.

        Returns:
            str: The received message.
        """
        receivedMessage = await asyncio.get_running_loop().run_in_executor(
            None, self._serialConnection.read
        )
        receivedMessage = receivedMessage.decode()
        return receivedMessage

    def close(self) -> None:
        """
        Close the serial connection.
        """
        self._serialConnection.close()
