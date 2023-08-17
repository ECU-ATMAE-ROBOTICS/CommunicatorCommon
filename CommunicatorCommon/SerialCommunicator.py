# Built-in
import logging
import asyncio
from typing import Optional
from serial import Serial
import time

# Exceptions
from .src.exceptions.SerialPortSetupError import SerialPortSetupError

# Internal
from .src.Event import Event


class SerialCommunicator:
    logger = logging.getLogger(__name__)
    START_MARKER = "<"
    END_MARKER = ">"

    def __init__(
        self,
        receiveTimeout: int = 1,
        readyVerification: str = None,
    ) -> None:
        """
        Initializes the CombinedSerialCommunicator.

        Args:
            receiveTimeout (int): How long the receiveMsg method will listen before returning the msg.
            readyVerification (str): Verification string for connection readiness.
        """
        self.eventQueue = asyncio.Queue()

        self.receiveTimeout = receiveTimeout
        self.readyVerification = readyVerification
        self.serialPort = None

    async def listenForEvents(self) -> Optional[any]:
        """Listens for events"""
        while True:
            event = await self.eventQueue.get()
            match event.eventType:
                case "send":
                    await self.sendMsg(event.data)
                case "receive":
                    await self.receiveMsg()
                case default:
                    return

    async def sendMsgEvent(self, msg):
        await self.eventQueue.put(Event("send", msg))

    async def receiveMsgEvent(self):
        await self.eventQueue.put(Event("receive"))

    async def setupSerial(
        self,
        baudRate: str = "9600",
        serialPortName: str = "/dev/ttyACM0",
    ) -> None:
        """
        Sets up the serial port for communication.
        """
        try:
            self.serialPort = Serial(
                port=serialPortName, baudrate=baudRate, timeout=0, rtscts=True
            )
            await self.waitForConnection()
        except Exception as e:
            raise SerialPortSetupError("Error setting up serial port") from e

    async def sendMsg(self, msg: str) -> None:
        """
        Sends a message through the serial connection.

        Args:
            msg (str): Message to send.
        """
        messageWithMarkers = self.START_MARKER + msg + self.END_MARKER
        self.serialPort.write(messageWithMarkers.encode("utf-8"))

    async def receiveMsg(self) -> str:
        msg = ""
        timeoutSeconds = self.receiveTimeout
        startTime = time.time()

        while time.time() - startTime < timeoutSeconds:
            char = await asyncio.to_thread(self.serialPort.read, 1)
            if char:
                charStr = char.decode("utf-8")
                msg += charStr

        return msg

    async def waitForConnection(self) -> None:
        """
        Waits for the device to signal it is ready for communication.
        """
        SerialCommunicator.logger.logging.info("Waiting for connection")
        msg = ""
        while not msg.startswith(self.readyVerification):
            msg = await self.receiveMsg()
            if msg:
                SerialCommunicator.logger.logging.info("Device connection established")
                break

    def closeSerial(self) -> None:
        """
        Closes the serial port.
        """
        if self.serialPort:
            self.serialPort.close()
            self.serialPort = None
