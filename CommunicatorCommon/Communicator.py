# Built-in
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="CommunicatorCommon/log/logs.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Internal
from .src.Auditory import Auditory


class Communicator(Auditory):
    logger = logging.getLogger(__name__)

    def __init__(
        self, baudRate: str = "9600", serialPortName: str = "/dev/ttyACM0"
    ) -> None:
        super().__init__(baudRate, serialPortName)

    def sendMsg(self, msg: str) -> None:
        """Sends a message through the serial connection

        Args:
            msg (str): Message to send
        """
        self.sendSerial(msg)

    def recieveMsg(self) -> str:
        """Listens for a message from the serial connection until a full message is recieved

        Returns:
            str: Message recieved
        """
        while True:
            msg = self.recvSerial()
            if msg:
                return msg
