# Internal
from .src.Auditory import Auditory


class Communicator(Auditory):
    def __init__(
        self, baudRate: str = "9600", serialPortName: str = "/dev/ttyACM0"
    ) -> None:
        super().__init__(baudRate, serialPortName)

    def send(self, msg: str) -> None:
        """Sends a message through the serial connection

        Args:
            msg (str): Message to send
        """
        self.__sendToArduino(msg)

    def recieve(self) -> str:
        """Listens for a message from the serial connection until a full message is recieved

        Returns:
            str: Message recieved
        """
        while True:
            msg = self.__recvLikeArduino()
            if not (msg == "XXX"):
                return msg
