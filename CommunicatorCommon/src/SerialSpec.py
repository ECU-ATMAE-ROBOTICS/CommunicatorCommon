# Built-in
import logging

# Third Party
from serial import Serial


class SerialSpec:
    logger = logging.getLogger(__name__)

    START_MARKER = "<"
    END_MARKER = ">"

    def __init__(
        self,
        readyVerification: str = None,
    ) -> None:
        """Constructor for SerialSpec

        Args:.
            readyVerification (str, optional): The message expected to be recieved by the other device to establish
            that it's ready for commmunication. Defaults to None.
        """
        self.readyVerification = readyVerification
        self.dataStarted = False
        self.dataBuf = ""
        self.messageComplete = False
        self.serialPort = None

    def setupSerial(
        self, baudRate: str = "9600", serialPortName: str = "/dev/ttyACM0"
    ) -> None:
        """Intialize the Serial Connection

        Args:
            baudRate (str, optional): The baudrate of the serial connection. Defaults to "9600".
            serialPortName (str, optional): The port to open the serial connection on. Defaults to "/dev/ttyACM0".
        """
        self.serialPort = Serial(
            port=serialPortName, baudrate=baudRate, timeout=0, rtscts=True
        )
        SerialSpec.logger.info(
            f"Serial port {serialPortName} opened Baudrate {baudRate}"
        )

        self.waitForConnection()

    def sendSerial(self, stringToSend: str) -> None:
        """Creates a "packet" to write into the serial

        Args:
            stringToSend (str): The string msg to send
        """
        stringWithMarkers = SerialSpec.START_MARKER
        stringWithMarkers += stringToSend
        stringWithMarkers += SerialSpec.END_MARKER

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
                if x != SerialSpec.END_MARKER:
                    self.dataBuf = self.dataBuf + x
                else:
                    self.dataStarted = False
                    self.messageComplete = True
            elif x == SerialSpec.START_MARKER:
                self.dataBuf = ""
                self.dataStarted = True

        if self.messageComplete:
            self.messageComplete = False
            return self.dataBuf
        else:
            return ""

    def waitForConnection(self) -> None:
        """Waits for the device to signal it is ready for communication"""
        SerialSpec.logger.info("Waiting for connection")

        msg = ""
        while not msg.startswith(self.readyVerification):
            msg = self.recvSerial()
            if msg:
                SerialSpec.logger.info("Device connection established")
                break
