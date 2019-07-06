from drivers.generic_driver_pymodbus import generic_driver_pymodbus as Driver
import logging
import time

logging.basicConfig()
log = logging.getLogger()
# log.setLevel(logging.DEBUG)

class S8000(Driver):
    def __init__(self,spec):
        spec_test = {"address": 1, "port": "COM19",
            "baudrate":9600, "parity":"None",
            "databits":8, "stopbits":2, "flowcontrol":"None"}
        Driver.__init__(self,spec_test)

    def read_dew_point(self):
        val = self.read_instrument(1,2)
        val = self._to_float(val)
        return val
    
    def read_sens_temp(self):
        val = self.read_instrument(20,1)
        val = self._to_int(val)
        return val

    def read_flow(self):
        val = self.read_instrument(15,1)
        return val

def main():
    inst = S8000({1:"2"})
    x = 1
    print (x)
    while x < 20:
        x+=1
        print(x)
        i = inst.read_dew_point()
        print(i)
        print(inst.read_flow())

if __name__ == "__main__":
    main()
