# Third Party
from mockito import when, mock, unstub, verify
from pytest import fixture
import serial

# Internal
from CommunicatorCommon import Communicator
from CommunicatorCommon.src import Auditory


mockAuditory = mock(Auditory)
when(Auditory).Auditory(..., ..., ...).thenReturn(mockAuditory)

mockSerial = mock(serial.Serial)
when(serial).Serial(...).thenReturn(mockSerial)
when(mockSerial).write(...).thenReturn(None)
when(mockSerial).read().thenReturn("Test Message")


# TODO Fix issues with stubbing the interactions with the serial port
@fixture
def communicator():
    return Communicator.Communicator()


@fixture
def auditory():
    return Auditory.Auditory()


def test_SendMsg(communicator):
    when(mockAuditory).sendSerial("Test Message").thenReturn(None)

    communicator.sendMsg("Test Message")
    verify(mockAuditory, times=1).sendSerial("Test Message")


def test_RecieveMsg(communicator):
    when(mockAuditory).recvSerial().thenReturn("Received Message")

    result = communicator.receiveMsg()
    verify(mockAuditory, times=1).recvSerial()
    assert result == "Received Message"


def test_SetupSerial(auditory):
    when(auditory).waitForConnection().thenReturn(None)

    auditory.setupSerial("9600", "/dev/ttyACM0")
    verify(serial).Serial(port="/dev/ttyACM0", baudrate="9600", timeout=0, rtscts=True)
    verify(auditory, times=1).waitForConnection()


unstub()
