# Third Party
import serial


class Auditory:
    __START_MARKER = "<"
    __END_MARKER = ">"

    def __init__(
        self, baudRate: str = "9600", serialPortName: str = "/dev/ttyACM0"
    ) -> None:
        self.listening = False
        self.dataStarted = False
        self.dataBuf = ""
        self.messageComplete = False
        self.serialPort = None
        self.__parse_file(baudRate, serialPortName)

    def __parse_file(self, baudRate: str, serialPortName: str) -> None:
        """Initializes serial upon class initialization

        Args:
            baudRate (str): _description_
            serialPortName (str): _description_
        """
        self.__setupSerial(baudRate, serialPortName)

    def __setupSerial(self, baudRate: str, serialPortName: str) -> None:
        """Initialize the serial and wait for the Arduino to be ready

        Args:
            baudRate (str): Baudrate of the serial connection
            serialPortName (str): Port that the serial is connected to
        """
        self.serialPort = serial.Serial(
            port=serialPortName, baudrate=baudRate, timeout=0, rtscts=True
        )

        print("Serial port " + serialPortName + " opened  Baudrate " + str(baudRate))
        self.__waitForArduino()

    def __sendToArduino(self, stringToSend: str) -> None:
        """Creates a "packet" to write into the serial

        Args:
            stringToSend (str): The string msg to send
        """
        stringWithMarkers = Auditory.__START_MARKER
        stringWithMarkers += stringToSend
        stringWithMarkers += Auditory.__END_MARKER

        self.serialPort.write(
            stringWithMarkers.encode("utf-8")
        )  # encode needed for Python3

    def __recvLikeArduino(self) -> str:
        """Reads a char from the arduino, building the message.
        NOTE: This method does not contain the logic to iterate until the message is complete. That should be
        implemented by whatever calls this

        Returns:
            str: Message recieved by the Arduino
        """
        if (
            self.serialPort.inWaiting() > 0
            and self.messageComplete == False
            or self.listening is True
        ):
            x = self.serialPort.read().decode(
                "utf-8", errors="replace"
            )  # decode needed for Python3

            if self.dataStarted == True:
                if x != Auditory.__END_MARKER:
                    self.dataBuf = self.dataBuf + x
                else:
                    self.dataStarted = False
                    self.messageComplete = True
            elif x == Auditory.__START_MARKER:
                self.dataBuf = ""
                self.dataStarted = True

        if self.messageComplete == True:
            self.messageComplete = False
            return self.dataBuf
        else:
            return "XXX"  # Message is not done when this is returned

    def __waitForArduino(self) -> None:
        """Waits for the Arduino to signal it is ready for communication"""
        print("Waiting for Arduino to reset")

        msg = ""
        while (
            msg.find("Arduino is ready") == -1
        ):  # This msg should be sent from the arduino to signal being ready
            msg = self.recvLikeArduino()
            if not (msg == "XXX"):
                print(msg)
