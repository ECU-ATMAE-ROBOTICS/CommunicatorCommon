# Built-in
import logging
import asyncio
from serial import Serial

# Exceptions
from .src.exceptions.SerialPortSetupException import SerialPortSetupException
from .src.exceptions.SerialCommunicationException import SerialCommunicationException

# Internal
from .src.CommunicatorEvent import CommunicatorEvent


class SerialCommunicator:
    logger = logging.getLogger(__name__)
    START_MARKER = b"<"
    END_MARKER = b">"

    def __init__(self, receiveTimeout: int = 1) -> None:
        """
        Initializes the SerialCommunicator.

        Args:
            receiveTimeout (int): How long the receiveMsg method will listen before returning the msg.
        """
        self.eventQueue = asyncio.Queue()
        self.serialReader = None
        self.receiveTimeout = receiveTimeout
        self.serialPort = None

    async def listenForEvents(self) -> None:
        """
        Listens for events and handles them.
        """
        while True:
            event = await self.eventQueue.get()
            if event.eventType == "send":
                await self.sendMsg(event.data)
            elif event.eventType == "receive":
                await self.receiveMsg()
            else:
                return

    async def sendMsgEvent(self, msg: str) -> None:
        """
        Adds a send event to the event queue.

        Args:
            msg (str): Message content to send.
        """
        await self.eventQueue.put(CommunicatorEvent("send", msg))

    async def receiveMsgEvent(self) -> None:
        """
        Adds a receive event to the event queue.
        """
        await self.eventQueue.put(CommunicatorEvent("receive"))

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
                asyncio.StreamReader, loop=self.eventQueue._loop
            )
            self.serialReaderProtocol = asyncio.StreamReaderProtocol(self.serialReader)
            self.serialReaderTransport, _ = await asyncio.to_thread(
                self.eventQueue._loop.connect_read_pipe,
                lambda: self.serialReaderProtocol,
                self.serialPort,
            )
            if waitForConnection:
                await self.waitForConnection()
        except Exception as e:
            raise SerialPortSetupException("Error setting up serial port") from e

    async def sendMsg(self, msg: str) -> None:
        """
        Sends a message through the serial connection in the specified format.

        Args:
            msg (str): Message content to send.
        """
        logger = logging.getLogger(__name__)

        message_size = len(msg)
        message_to_send = f"<{message_size:04}{msg}>"
        try:
            self.serialPort.write(message_to_send.encode("utf-8"))
        except Exception as e:
            logger.error(f"Error while sending message: {e}")
            raise SerialCommunicationException()

    async def receiveMsg(self) -> str:
        """
        Receives a message from the serial connection.

        Returns:
            str: The received message content.
        """
        start_marker_found = False
        while not start_marker_found:
            data = await self.serialReader.read(1)
            if data == SerialCommunicator.START_MARKER:
                start_marker_found = True

        msg_size_str = b""
        while True:
            char = await self.serialReader.read(1)
            if char == SerialCommunicator.END_MARKER:
                break
            msg_size_str += char
        msg_size = int(msg_size_str)

        try:
            msg_content = await self.serialReader.read(msg_size)
        except TimeoutError as te:
            SerialCommunicator.logger.error("Timeout while reading message content.")
            raise te

        if len(msg_content) != msg_size:
            SerialCommunicator.logger.error("Received incomplete message content.")
            raise ValueError("Received incomplete message content.")

        return msg_content.decode("utf-8")

    async def waitForConnection(
        self,
        readyVerification: str = None,
    ) -> None:
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
