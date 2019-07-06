from generic_driver_pymodbus_async import generic_driver_pymodbus as Driver
import asyncio
import logging
import time

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class HMP4(Driver):
    def __init__(self):
        spec = {"address": 240, "port": "COM4",
            "baudrate":19200, "parity":"None",
            "databits":8, "stopbits":2, "flowcontrol":"None"}
        print("here2")
        Driver.__init__(self,spec)
        self.mainloop = asyncio.get_event_loop()

    def read_signed_int_test(self):
        self.mainloop.run_until_complete(self._read_signed_int_test())
    
    async def _read_signed_int_test(self):
        print("print")
        try:
           val = await asyncio.wait_for(self.read_instrument(7936), timeout=20.0)
        except asyncio.TimeoutError:
            print('timeout!')
        
        # val = await self.read_instrument(7936)
        val = self._to_int(val)
        print(val)

    def read_float_test(self):
        self.mainloop.run_until_complete(self._read_float_test())
    
    async def _read_float_test(self):
        print("print")
        try:
           val = await asyncio.wait_for(self.read_instrument(7937,2), timeout=20.0)
        except asyncio.TimeoutError:
            print('timeout!')
        
        # val = await self.read_instrument(7936)
        val= self._to_float(val)
        print(val)

        

async def main():
    inst = HMP4()
    print(inst)
    await asyncio.sleep(2)
    inst.read_signed_int_test()
    inst.read_float_test()
    # inst.read_signed_int_test()
    response =  asyncio.gather(inst._read_signed_int_test, inst._read_float_test)
    # print(response.result())

if __name__ == "__main__":
    asyncio.run(main())
