from drivers.generic_driver_pymodbus import generic_driver_pymodbus as Driver
import logging
import time

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


class HMP4(Driver):
    lock = None
    def __init__(self,spec):
        spec_test = {"address": 240, "port": "COM4",
            "baudrate":19200, "parity":"None",
            "databits":8, "stopbits":2, "flowcontrol":"None"}
        Driver.__init__(self,spec_test)

    def read_signed_int_test(self):
        val = self.read_instrument(7936)
        val = self._to_int(val)
        return val
    
    def read_float_test(self):
        val = self.read_instrument(7937,2)
        val= self._to_float(val)
        return val

        

def main():
    inst = HMP4()
    i = inst.read_signed_int_test()
    f =inst.read_float_test()
    print(i,f)
    

if __name__ == "__main__":
    main()
