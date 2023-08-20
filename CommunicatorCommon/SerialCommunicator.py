# Built-in
import logging
import asyncio
from serial import Serial

# Exceptions
from .src.exceptions.SerialPortSetupException import SerialPortSetupException
from .src.exceptions.SerialCommunicationException import SerialCommunicationException


class SerialCommunicator:
    """
    A class for serial communication handling.

    Args:
        receiveTimeout (int): How long the receiveMsg method will listen before returning the msg.
    """

    logger = logging.getLogger(__name__)
    startMarker = b"<"
    endMarker = b">"

    def __init__(self, receiveTimeout: int = 1) -> None:
        """
        Initializes the SerialCommunicator.

        Args:
            receiveTimeout (int): How long the receiveMsg method will listen before returning the msg.
        """
        self.serialPort = None
        self.receiveTimeout = receiveTimeout

    async def setupSerial(
        self,
        baudRate: int = 9600,
        serialPortName: str = "/dev/ttyACM0",
        waitForConnection: bool = False,
    ) -> None:
        """
        Sets up the serial port for communication.

        Args:
            baudRate (int): Baud rate for serial communication.
            serialPortName (str): Name of the serial port.
            waitForConnection (bool): Whether to wait for the connection to be established.
        """
        try:
            self.serialPort = Serial(
                port=serialPortName, baudrate=baudRate, timeout=0, rtscts=True
            )

            self.serialReader, _ = await asyncio.to_thread(
                asyncio.StreamReader, loop=asyncio.get_event_loop()
            )
            self.serialReaderProtocol = asyncio.StreamReaderProtocol(self.serialReader)
            self.serialReaderTransport, _ = await asyncio.to_thread(
                asyncio.get_event_loop().connect_read_pipe,
                lambda: self.serialReaderProtocol,
                self.serialPort,
            )
            if waitForConnection:
                await self._waitForConnection()
        except Exception as e:
            raise SerialPortSetupException("Error setting up serial port") from e

    async def sendMsg(self, msg: str) -> None:
        """
        Sends a message through the serial connection in the specified format.

        Args:
            msg (str): Message content to send.
        """

        messageSize = len(msg)
        messageToSend = f"<{messageSize:04}{msg}>"
        try:
            self.serialPort.write(messageToSend.encode("utf-8"))
        except Exception as e:
            SerialCommunicator.logger.error(f"Error while sending message: {e}")
            raise SerialCommunicationException()

    async def receiveMsg(self) -> str:
        """
        Receives a message from the serial connection.

        Returns:
            str: The received message content.
        """
        startMarkerFound = False
        while not startMarkerFound:
            data = await self.serialReader.read(1)
            if data == SerialCommunicator.startMarker:
                startMarkerFound = True

        msgSizeStr = b""
        while True:
            char = await self.serialReader.read(1)
            if char == SerialCommunicator.endMarker:
                break
            msgSizeStr += char
        msgSize = int(msgSizeStr)

        try:
            msgContent = await self.serialReader.read(msgSize)
        except TimeoutError as te:
            SerialCommunicator.logger.error("Timeout while reading message content.")
            raise te

        if len(msgContent) != msgSize:
            SerialCommunicator.logger.error("Received incomplete message content.")
            raise ValueError("Received incomplete message content.")

        return msgContent.decode("utf-8")

    async def _waitForConnection(self, readyVerification: str = None) -> None:
        """
        Waits for the connection to be established.

        Args:
            readyVerification (str): Verification string for connection readiness.
        """
        SerialCommunicator.logger.info("Waiting for connection")
        msg = ""
        while not msg.startswith(readyVerification):
            msg = await self.receiveMsg()
            if msg:
                SerialCommunicator.logger.info("Device connection established")
                break

    def closeSerial(self) -> None:
        """
        Closes the serial port.
        """
        if self.serialPort:
            self.serialPort.close()
            self.serialPort = None
