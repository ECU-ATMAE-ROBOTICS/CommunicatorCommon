"""Tests for the ISerialCommunicator module."""

from unittest.mock import Mock, patch
import pytest
from CommunicatorCommon import SerialCommunicator


@pytest.fixture
def mock_serial():
    """Fixture to create a mock for the serial.Serial object."""
    return Mock()


@patch("CommunicatorCommon.serial_communicator.serial.Serial", autospec=True)
def test_init(mock_serial_class, mock_serial):
    """
    Test the initialization of SerialCommunicator.
    Verifies that the serial.Serial class is called with the correct default
    parameters.
    """
    mock_serial_class.return_value = mock_serial
    _ = SerialCommunicator()
    mock_serial_class.assert_called_once_with("dev/ttyACM0", 9600)


@patch("CommunicatorCommon.serial_communicator.serial.Serial", autospec=True)
def test_send_message(mock_serial_class, mock_serial):
    """
    Test sending a message through the SerialCommunicator.
    Ensures that the message is encoded and written to the serial port correctly.
    """
    mock_serial_class.return_value = mock_serial
    communicator = SerialCommunicator()
    message = "test message"
    communicator.send_msg(message)
    mock_serial.write.assert_called_once_with(message.encode())


@patch("CommunicatorCommon.serial_communicator.serial.Serial", autospec=True)
def test_receive_message(mock_serial_class, mock_serial):
    """
    Test receiving a message through the SerialCommunicator.
    Checks that the serial port's read method is called and the result is
    decoded correctly.
    """
    mock_serial_class.return_value = mock_serial
    communicator = SerialCommunicator()
    mock_serial.read.return_value = b"test"
    received_message = communicator.receive_msg()
    mock_serial.read.assert_called_once()
    assert received_message == "test"


@patch("CommunicatorCommon.serial_communicator.serial.Serial", autospec=True)
def test_receive_message_with_timeout(mock_serial_class, mock_serial):
    """
    Test receiving a message through the SerialCommunicator utilizing a timeout.
    Checks that the serial port's read method is called and the result is
    decoded correctly.
    """
    mock_serial_class.return_value = mock_serial
    communicator = SerialCommunicator()
    mock_serial.read.return_value = b"test"
    received_message = communicator.receive_msg(timeout=5)
    mock_serial.read.assert_called_once()
    assert received_message == "test"


@patch("CommunicatorCommon.serial_communicator.serial.Serial", autospec=True)
def test_receive_message_none(mock_serial_class, mock_serial):
    """
    Test receiving a message through the SerialCommunicator utilizing a timeout.
    Checks that the serial port's read method is called and the result is
    decoded correctly.
    """
    mock_serial_class.return_value = mock_serial
    communicator = SerialCommunicator()
    mock_serial.read.return_value = None
    received_message = communicator.receive_msg()
    mock_serial.read.assert_called_once()
    assert received_message == None


@patch("CommunicatorCommon.serial_communicator.serial.Serial", autospec=True)
def test_close(mock_serial_class, mock_serial):
    """
    Test the close method of SerialCommunicator.
    Ensures that the serial connection is closed properly.
    """
    mock_serial_class.return_value = mock_serial
    communicator = SerialCommunicator()
    communicator.close()
    mock_serial.close.assert_called_once()
