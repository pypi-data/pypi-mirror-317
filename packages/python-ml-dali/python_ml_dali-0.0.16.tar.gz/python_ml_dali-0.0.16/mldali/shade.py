from .controller import MLDaliController
from .const import SHADE_CLOSING, SHADE_OPENING, SHADE_OPENED, SHADE_CLOSED, SHADE_STOPPED, UNKNOWN_EVENT
import logging
import asyncio

_LOGGER = logging.getLogger(__name__)

class MLDaliShade():

    def __init__(self, address, port="COM4", full_close_duration = 50, group_membership = []):
        self.address = address
        self._controller = MLDaliController.register(self,port=port)
        for group_address in group_membership:
            self._controller.registerToGroup(group_address, self)
        self.state = None
        self.pending_task = None
        self.full_close_duration = full_close_duration #Number of seconds for the shade to completely close/open
        self._listeners = []
    
    async def open(self):
        cmd = bytearray([0x01, (self.address*2)+1, 0x19, 0xC1])
        await self._controller.sendCmd(cmd)

    async def close(self):
        cmd = bytearray([0x01, (self.address*2)+1, 0x18, 0xC1])
        await self._controller.sendCmd(cmd)
    
    async def stop(self):
        cmd = bytearray([0x01, (self.address*2)+1, 0, 0xC1])
        await self._controller.sendCmd(cmd)        
    
    async def signal_completion(self, final_state):
        await asyncio.sleep(self.full_close_duration)
        self.state = final_state
        logging.info(f"Shade {self.address} changed state to {self.state}")
        self.pending_task = None
        for call in self._listeners:
            call(self.state)

    def status_update(self, rx):
        _LOGGER.debug(f"Component at address {self.address} received status_update: {rx}")

        if self.pending_task:
            self.pending_task.cancel()

        if rx[2:3] == b'\x19':
            self.state = SHADE_OPENING
            self.pending_task = asyncio.create_task(self.signal_completion(SHADE_OPENED))
        elif rx[2:3] == b'\x18':
            self.state = SHADE_CLOSING
            self.pending_task = asyncio.create_task(self.signal_completion(SHADE_CLOSED))
        elif rx[2:3] == b'\x00':
            self.state = SHADE_STOPPED
        else:
            self.state = UNKNOWN_EVENT
        
        _LOGGER.info(f"Shade {self.address} changed state to {self.state}")
        
        for call in self._listeners:
            call(self.state)
    
    def registerEventListener(self, callable):
        self._listeners.append(callable)