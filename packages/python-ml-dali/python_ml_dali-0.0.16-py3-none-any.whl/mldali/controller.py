import aioserial
import asyncio
import serial
#import time

import logging
_LOGGER = logging.getLogger(__name__)

class MLDaliController:
    __instance__ = None

    def __init__(self, port, baudrate, parity, stopbits, bytesize, timeout):
        """ Constructor.
        """

        if MLDaliController.__instance__ is None:
            self._ser = aioserial.AioSerial(
                                        port = port,
                                        baudrate = baudrate,
                                        timeout = timeout,
                                        parity = parity,
                                        stopbits = stopbits,
                                        bytesize = bytesize
                                    )
            self._registry = {}
            self._groups = {}        
            MLDaliController.__instance__ = self
   
    @staticmethod
    def register(component, port = "COM4", 
                    baudrate = 9600, 
                    parity = serial.PARITY_NONE, 
                    stopbits = serial.STOPBITS_ONE, 
                    bytesize = serial.EIGHTBITS, 
                    timeout = None) -> 'MLDaliController':
        if not MLDaliController.__instance__:
            MLDaliController(port, baudrate, parity, stopbits, bytesize, timeout)
            asyncio.create_task(MLDaliController.__instance__.monitor())
        MLDaliController.__instance__._registry[(component.address*2)+1] = component
        return MLDaliController.__instance__


    def open(self):
        self._ser.open()
    
    def close(self):
        self._ser.close()
    
    async def monitor(self):
        _LOGGER.debug("Start Monitoring")
        cmd = bytes()
        while True:
            rx = await self._ser.read_async(1)
            logging.debug(f"Observed: {rx}")
            if rx == b'\x02' or rx == b'\x04':
                cmd = rx
            else:
                cmd += rx
            
            if len(cmd) == 3:
                address = int.from_bytes(cmd[1:2],'big')
                if address >= 129 and address <= 159:
                    address_list = self._getGroupDevices(address)
                else:
                    address_list = [address]
                
                for addr in address_list:
                    component = self._registry.get(addr, None)
                    if component:
                        component.status_update(cmd)

    async def read_byte(self):
        rx = await self._ser.read_async(3)
        return rx
    
    async def sendCmd(self, tx):
        await self._ser.write_async(tx)
        #time.sleep(.1)
        await asyncio.sleep(.1)

    def registerToGroup(self, group_address, component):
        internal_group_address = (group_address*2)+1
        if internal_group_address not in self._groups:
            self._groups[internal_group_address] = set()
        self._groups[internal_group_address].add((component.address*2)+1)

    def removeFromGroup(self, group_address, component):
        internal_group_address = (group_address*2)+1
        if internal_group_address in self._groups:
            self._groups[internal_group_address].discard((component.address*2)+1)

    def _getGroupDevices(self, internal_group_address):
        return list(self._groups.get(internal_group_address, set()))
