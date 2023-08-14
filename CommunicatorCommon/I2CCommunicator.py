# Built-in
import logging


logging.basicConfig(
    level=logging.INFO,
    filename="CommunicatorCommon/log/logs.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class I2CCommuncatior:
    def __init__(self) -> None:
        pass
