# Built-in
import logging

# Third Party
from serial import Serial


logging.basicConfig(
    level=logging.INFO,
    filename="CommunicatorCommon/log/logs.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class Auditory:
    logger = logging.getLogger(__name__)

    START_MARKER = "<"
    END_MARKER = ">"

    def __init__(
        self,
        baudRate: str = "9600",
        serialPortName: str = "/dev/ttyACM0",
        readyVerification: str = None,
    ) -> None:
        """Constructor for Auditory

        Args:
            baudRate (str, optional):The baudrate to establish the serial connection with. Defaults to "9600".
            serialPortName (str, optional): The port name to establish the serial connection on. Defaults to "/dev/ttyACM0".
            readyVerification (str, optional): The message expected to be recieved by the other device to establish
            that it's ready for commmunication. Defaults to None.
        """
        self.readyVerification = readyVerification
        self.dataStarted = False
        self.dataBuf = ""
        self.messageComplete = False
        self.serialPort = None
        self.parseFile(baudRate, serialPortName)

    def parseFile(self, baudRate: str, serialPortName: str) -> None:
        """Initializes serial upon class initialization

        Args:
            baudRate (str): Baudrate of the serial connection
            serialPortName (str): Port that the serial is connected to
        """
        self.setupSerial(baudRate, serialPortName)

    def setupSerial(self, baudRate: str, serialPortName: str) -> None:
        """Initialize the serial and wait for the Arduino to be ready

        Args:
            baudRate (str): Baudrate of the serial connection
            serialPortName (str): Port that the serial is connected to
        """
        self.serialPort = Serial(
            port=serialPortName, baudrate=baudRate, timeout=0, rtscts=True
        )
        Auditory.logger.info(f"Serial port {serialPortName} opened Baudrate {baudRate}")

        self.waitForConnection()

    def sendSerial(self, stringToSend: str) -> None:
        """Creates a "packet" to write into the serial

        Args:
            stringToSend (str): The string msg to send
        """
        stringWithMarkers = Auditory.START_MARKER
        stringWithMarkers += stringToSend
        stringWithMarkers += Auditory.END_MARKER

        self.serialPort.write(
            stringWithMarkers.encode("utf-8")
        )  # encode needed for Python3

    def recvSerial(self) -> str:
        """Reads a char from the device, building the message.
        NOTE: This method does not contain the logic to iterate until the message is complete. That should be
        implemented by whatever calls this

        Returns:
            str: Message recieved by the device
        """
        if self.serialPort.inWaiting() > 0 and not self.messageComplete:
            x = self.serialPort.read().decode(
                "utf-8", errors="replace"
            )  # decode needed for Python3

            if self.dataStarted:
                if x != Auditory.END_MARKER:
                    self.dataBuf = self.dataBuf + x
                else:
                    self.dataStarted = False
                    self.messageComplete = True
            elif x == Auditory.START_MARKER:
                self.dataBuf = ""
                self.dataStarted = True

        if self.messageComplete:
            self.messageComplete = False
            return self.dataBuf
        else:
            return ""

    def waitForConnection(self) -> None:
        """Waits for the device to signal it is ready for communication"""
        Auditory.logger.info("Waiting for connection")

        msg = ""
        while msg.find(self.readyVerification) == -1:
            msg = self.recvSerial()
            if msg:
                Auditory.logger.info("Device connection established")
