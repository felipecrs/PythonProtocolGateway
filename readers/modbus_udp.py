import logging
from protocol_settings import Registry_Type
from pymodbus.client.sync import ModbusUdpClient
from .reader_base import reader_base

class modbus_udp(reader_base):
    port : int = 502
    host : str = ""
    client : ModbusUdpClient 

    def __init__(self, settings : dict[str,str]):
        #logger = logging.getLogger(__name__)
        #logging.basicConfig(level=logging.DEBUG)

        if "port" in settings:
            self.port = settings["port"]

        if "host" in settings:
            self.host = settings["host"]

        if not self.host:
            raise ValueError("Host is not set")

        self.client = ModbusUdpClient(host=self.host, port=self.port, timeout=7, retries=3)
        
    def read_registers(self, start, count=1, registry_type : Registry_Type = Registry_Type.INPUT, **kwargs):
        if registry_type == Registry_Type.INPUT:
            return self.client.read_input_registers(start, count, **kwargs)
        elif registry_type == Registry_Type.HOLDING:
            return self.client.read_holding_registers(start, count, **kwargs)

    def connect(self):
        self.client.connect()