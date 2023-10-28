import pytest
from unittest.mock import Mock, patch
from CommunicatorCommon.I2CCommunicator import I2CCommunicator


@pytest.fixture
def mock_smbus():
    return Mock()


@patch("CommunicatorCommon.I2CCommunicator.smbus2.SMBus", autospec=True)
def testInit(mock_smbus_class, mock_smbus):
    mock_smbus_class.return_value = mock_smbus
    communicator = I2CCommunicator()
    mock_smbus_class.assert_called_once_with(1)
    assert communicator._busId == 1


@patch("CommunicatorCommon.I2CCommunicator.smbus2.SMBus", autospec=True)
def testSendMsg(mock_smbus_class, mock_smbus):
    mock_smbus_class.return_value = mock_smbus
    communicator = I2CCommunicator()
    address = 8
    msg = b"test message"
    communicator.sendMsg(address, msg)
    mock_smbus.write_i2c_block_data.assert_called_once_with(address, 0, list(msg))


@patch("CommunicatorCommon.I2CCommunicator.smbus2.SMBus", autospec=True)
def testReceiveMsg(mock_smbus_class, mock_smbus):
    mock_smbus_class.return_value = mock_smbus
    communicator = I2CCommunicator()
    address = 8
    length = 5
    mock_smbus.read_i2c_block_data.return_value = [1, 2, 3, 4, 5]
    received_msg = communicator.receiveMsg(address, length)
    mock_smbus.read_i2c_block_data.assert_called_once_with(address, 0, length)
    assert received_msg == bytes([1, 2, 3, 4, 5])


@patch("CommunicatorCommon.I2CCommunicator.smbus2.SMBus", autospec=True)
def testSendMsgException(mock_smbus_class, mock_smbus):
    mock_smbus_class.return_value = mock_smbus
    communicator = I2CCommunicator()
    address = 8
    msg = b"test message"
    mock_smbus.write_i2c_block_data.side_effect = Exception("Test Exception")
    with pytest.raises(Exception) as e:
        communicator.sendMsg(address, msg)
    assert str(e.value) == "Test Exception"


@patch("CommunicatorCommon.I2CCommunicator.smbus2.SMBus", autospec=True)
def testReceiveMsgException(mock_smbus_class, mock_smbus):
    mock_smbus_class.return_value = mock_smbus
    communicator = I2CCommunicator()
    address = 8
    length = 5
    mock_smbus.read_i2c_block_data.side_effect = Exception("Test Exception")
    with pytest.raises(Exception) as e:
        communicator.receiveMsg(address, length)
    assert str(e.value) == "Test Exception"
