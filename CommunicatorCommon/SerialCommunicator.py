# Built-in
import logging

# Internal
from .src.SerialSpec import SerialSpec


class SerialCommunicator:
    logger = logging.getLogger(__name__)

    def __init__(
        self, baudRate: str = "9600", serialPortName: str = "/dev/ttyACM0"
    ) -> None:
        self.serialComm = SerialSpec(baudRate, serialPortName)

    def sendMsg(self, msg: str) -> None:
        """Sends a message through the serial connection

        Args:
            msg (str): Message to send
        """
        self.serialComm.sendSerial(msg)

    def receiveMsg(self) -> str:
        """Listens for a message from the serial connection until a full message is recieved

        Returns:
            str: Message recieved
        """
        while True:
            msg = self.serialComm.recvSerial()
            if msg:
                return msg
