"""Tests for the I2CCommunicator module."""

from unittest.mock import Mock, patch
import pytest
from CommunicatorCommon import I2CCommunicator


@pytest.fixture
def mock_smbus():
    """Fixture to mock SMBus object."""
    return Mock()


@patch("CommunicatorCommon.i2c_communicator.smbus2.SMBus", autospec=True)
def test_init(mock_smbus_class, mock_smbus):
    """Test initialization of I2CCommunicator verifies bus ID is set correctly."""
    mock_smbus_class.return_value = mock_smbus
    communicator = I2CCommunicator()
    mock_smbus_class.assert_called_once_with(1)
    assert communicator._bus_id == 1


@patch("CommunicatorCommon.i2c_communicator.smbus2.SMBus", autospec=True)
def test_send_msg(mock_smbus_class, mock_smbus):
    """Test sending a message through I2CCommunicator."""
    mock_smbus_class.return_value = mock_smbus
    communicator = I2CCommunicator()
    address = 8
    msg = b"test message"
    communicator.send_msg(address, msg)
    mock_smbus.write_i2c_block_data.assert_called_once_with(address, 0, list(msg))


@patch("CommunicatorCommon.i2c_communicator.smbus2.SMBus", autospec=True)
def test_receive_msg(mock_smbus_class, mock_smbus):
    """Test receiving a message through I2CCommunicator."""
    mock_smbus_class.return_value = mock_smbus
    communicator = I2CCommunicator()
    address = 8
    length = 5
    mock_smbus.read_i2c_block_data.return_value = [1, 2, 3, 4, 5]
    received_msg = communicator.receive_msg(address, length)
    mock_smbus.read_i2c_block_data.assert_called_once_with(address, 0, length)
    assert received_msg == bytes([1, 2, 3, 4, 5])


@patch("CommunicatorCommon.i2c_communicator.smbus2.SMBus", autospec=True)
def test_send_msg_exception(mock_smbus_class, mock_smbus):
    """Test exception handling when sending a message fails."""
    mock_smbus_class.return_value = mock_smbus
    communicator = I2CCommunicator()
    address = 8
    msg = b"test message"
    mock_smbus.write_i2c_block_data.side_effect = Exception("Test Exception")
    with pytest.raises(Exception) as e:
        communicator.send_msg(address, msg)
    assert str(e.value) == "Test Exception"


@patch("CommunicatorCommon.i2c_communicator.smbus2.SMBus", autospec=True)
def test_receive_msg_exception(mock_smbus_class, mock_smbus):
    """Test exception handling when receiving a message fails."""
    mock_smbus_class.return_value = mock_smbus
    communicator = I2CCommunicator()
    address = 8
    length = 5
    mock_smbus.read_i2c_block_data.side_effect = Exception("Test Exception")
    with pytest.raises(Exception) as e:
        communicator.receive_msg(address, length)
    assert str(e.value) == "Test Exception"
