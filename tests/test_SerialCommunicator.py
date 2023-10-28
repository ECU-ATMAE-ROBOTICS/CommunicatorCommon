import pytest
from unittest.mock import Mock, patch
from CommunicatorCommon.SerialCommunicator import SerialCommunicator


@pytest.fixture
def mock_serial():
    return Mock()


@patch("CommunicatorCommon.SerialCommunicator.serial.Serial", autospec=True)
def test_init(mock_serial_class, mock_serial):
    mock_serial_class.return_value = mock_serial
    communicator = SerialCommunicator()
    mock_serial_class.assert_called_once_with("dev/ttyACM0", 9600)


@patch("CommunicatorCommon.SerialCommunicator.serial.Serial", autospec=True)
def test_send_message(mock_serial_class, mock_serial):
    mock_serial_class.return_value = mock_serial
    communicator = SerialCommunicator()
    message = "test message"
    communicator.sendMessage(message)
    mock_serial.write.assert_called_once_with(message.encode())


@patch("CommunicatorCommon.SerialCommunicator.serial.Serial", autospec=True)
def test_receive_message(mock_serial_class, mock_serial):
    mock_serial_class.return_value = mock_serial
    communicator = SerialCommunicator()
    mock_serial.read.return_value = b"test"
    received_message = communicator.receiveMessage()
    mock_serial.read.assert_called_once()
    assert received_message == "test"


@patch("CommunicatorCommon.SerialCommunicator.serial.Serial", autospec=True)
def test_close(mock_serial_class, mock_serial):
    mock_serial_class.return_value = mock_serial
    communicator = SerialCommunicator()
    communicator.close()
    mock_serial.close.assert_called_once()
