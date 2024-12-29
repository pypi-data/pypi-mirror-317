# python-ml-dali
A Python library to communicate with Dali controllers from Ministry of Light

## Description
This python libarary can be used to communicate with ML (Ministry of Light) Dali relais on a DALI bus, using the ML DALI USB controller. 
## Documentation

## QuickStart

```python
import asyncio
from mldali import MLDaliLight

async def turnOnOff(address):
    light_fixture = MLDaliLight(address)
    await asyncio.sleep(1)
    await light_fixture.turn_on()
    await asyncio.sleep(3)
    await light_fixture.turn_off()

async def turnOnOffDelayed(address):
    await asyncio.sleep(2)
    light_fixture = MLDaliLight(address)
    await asyncio.sleep(1)
    await light_fixture.turn_on()
    await asyncio.sleep(1)
    await light_fixture.turn_off()


async def main():
    await asyncio.gather(turnOnOff(12), turnOnOffDelayed(13), asyncio.sleep(20))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

```

