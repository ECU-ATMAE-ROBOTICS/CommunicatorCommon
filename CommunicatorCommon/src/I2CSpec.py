# Built-in
import logging

# Third Party
from smbus2 import SMBus

logging.basicConfig(
    level=logging.INFO,
    filename="CommunicatorCommon/log/logs.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class I2CSpec:
    def __init__(self, busId: int = 1) -> None:
        self.i2cbus = SMBus(busId)
