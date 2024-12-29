from .controller import MLDaliController
from .const import LIGHT_SWITCHED_ON, LIGHT_SWITCHED_OFF, UNKNOWN_EVENT
#import time
import asyncio
import logging
_LOGGER = logging.getLogger(__name__)

class MLDaliLight():

    def __init__(self, address, port="COM4", group_membership = []):
        self.address = address
        self._controller = MLDaliController.register(self,port=port)
        for group_address in group_membership:
            self._controller.registerToGroup(group_address, self)
        self.is_on = False
        self._listeners = []
    
    async def turn_on(self):
        cmd = bytearray([0x01, (self.address*2)+1, 5, 0xC1])
        #time.sleep(.1) 
        await asyncio.sleep(.1) #This delay ensures that the command doesn't collapse with other commands being send on the bus
        await self._controller.sendCmd(cmd)

    
    async def turn_off(self):
        cmd = bytearray([0x01, (self.address*2)+1, 0, 0xC1])
        #time.sleep(.1)
        await asyncio.sleep(.1)
        await self._controller.sendCmd(cmd)
    
    def status_update(self, rx):
        _LOGGER.debug(f"Component at address {self.address} received status_update: {rx}")
        event = UNKNOWN_EVENT
        if rx[2:3] == b'\x05':
            self.is_on = True
            event = LIGHT_SWITCHED_ON
        elif rx[2:3] == b'\x00':
            self.is_on = False
            event = LIGHT_SWITCHED_OFF
        _LOGGER.info(f"Shade {self.address} changed state to {event}")
        for call in self._listeners:
            call(event)
    
    def registerEventListener(self, callable):
        self._listeners.append(callable)