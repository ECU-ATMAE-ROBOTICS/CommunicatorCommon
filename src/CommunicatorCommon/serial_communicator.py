"""Communicator for Serial Communication"""

from typing import Optional
import serial


class SerialCommunicator:
    """
    A class for communicating through a serial port.
    """

    def __init__(self, port: str = "dev/ttyACM0", baud_rate: int = 9600) -> None:
        """
        Initialize the SerialCommunicator class.

        Args:
            port (str): The name of the serial port to connect to.
            Default is "dev/ttyACM0".

            baud_rate (int): The baud rate for the serial communication.
            Default is 9600.
        """
        self._port = port
        self._baud_rate = baud_rate
        self._serial_connection = serial.Serial(port, baud_rate)

    def send_msg(self, message: str) -> None:
        """
        Send a message through the serial port.

        Args:
            message (str): The message to be sent.
        """
        encoded_message = message.encode()
        self._serial_connection.write(encoded_message)

    def receive_msg(self, timeout: Optional[float] = None) -> str | None:
        """
        Receive a message from the serial port.

        Args:
            timeout (Optional[float]): Timeout in seconds for the operation.
            If not provided, there is no timeout.

        Returns:
            str: The received message, or None if timeout is reached.

        Note:
            The function sets a temporary timeout for this specific read operation,
            if provided, and restores the original timeout after.
        """
        original_timeout = self._serial_connection.timeout
        try:
            if timeout is not None:
                self._serial_connection.timeout = timeout
            received_message = self._serial_connection.read()
            if received_message:
                return received_message.decode()
            return None
        finally:
            self._serial_connection.timeout = original_timeout

    def close(self) -> None:
        """
        Close the serial connection.
        """
        self._serial_connection.close()
