import unittest
from unittest.mock import patch, Mock

from CommunicatorCommon.src.SerialSpec import SerialSpec
from CommunicatorCommon.SerialCommunicator import SerialCommunicator


class TestSerialSpec(unittest.TestCase):
    @patch("CommunicatorCommon.src.SerialSpec.Serial")
    def testSendSerial(self, mockSerialClass):
        mockSerialInstance = mockSerialClass.return_value

        mockSerialInstance.inWaiting.return_value = 1

        serialSpecInstance = SerialSpec(readyVerification="ready")
        mockRecvSerial = Mock(side_effect="ready")
        serialSpecInstance.recvSerial = mockRecvSerial

        serialSpecInstance.setupSerial()

        mockRecvSerial.assert_called()

    # TODO Make this test useful
    @patch("CommunicatorCommon.SerialCommunicator.SerialSpec")
    def testSendMsg(self, mockSerialSpecClass):
        mockSerialSpecInstance = mockSerialSpecClass.return_value
        serialCommInstance = SerialCommunicator()
        serialCommInstance.serialComm = mockSerialSpecInstance

        serialCommInstance.sendMsg("test message")
        mockSerialSpecInstance.sendSerial.assert_called_once_with("test message")

    # TODO Make this test useful
    @patch("CommunicatorCommon.SerialCommunicator.SerialSpec")
    def testReceiveMsg(self, mockSerialSpecClass):
        mockSerialSpecInstance = mockSerialSpecClass.return_value
        serialCommInstance = SerialCommunicator()
        serialCommInstance.serialComm = mockSerialSpecInstance

        mockSerialSpecInstance.recvSerial.return_value = "test message"

        receivedMsg = serialCommInstance.receiveMsg()
        mockSerialSpecInstance.recvSerial.assert_called_once()
        self.assertEqual(receivedMsg, "test message")


if __name__ == "__main__":
    unittest.main()
