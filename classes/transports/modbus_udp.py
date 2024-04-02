import logging
from classes.protocol_settings import Registry_Type, protocol_settings
from pymodbus.client.sync import ModbusUdpClient
from .transport_base import transport_base
from configparser import SectionProxy


class modbus_udp(transport_base):
    port : int = 502
    host : str = ""
    client : ModbusUdpClient 

    def __init__(self, settings : SectionProxy, protocolSettings : protocol_settings = None):
        #logger = logging.getLogger(__name__)
        #logging.basicConfig(level=logging.DEBUG)

        self.host = settings.get("host", "")
        if not self.host:
            raise ValueError("Host is not set")
        
        self.port = settings.getint("port", self.port)

        self.client = ModbusUdpClient(host=self.host, port=self.port, timeout=7, retries=3)

        super().__init__(settings, protocolSettings=protocolSettings)
        
    def read_registers(self, start, count=1, registry_type : Registry_Type = Registry_Type.INPUT, **kwargs):
        if registry_type == Registry_Type.INPUT:
            return self.client.read_input_registers(start, count, **kwargs)
        elif registry_type == Registry_Type.HOLDING:
            return self.client.read_holding_registers(start, count, **kwargs)

    def connect(self):
        self.connected = self.client.connect()
        super().connect()