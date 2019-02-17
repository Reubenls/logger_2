from drivers.generic_driver_visa_gpib import generic_driver_visa_gpib as Driver
import logging
import time

logging.basicConfig()
log = logging.getLogger()
# log.setLevel(logging.DEBUG)

class F250_K705(Driver):
    def __init__(self,spec):
        spec_test = {"port_bridge": "GPIB0::3::INSTR",
                     "port_scanner": "GPIB0::17::INSTR",
                     "baudrate":9600,
                     "write_termination":"\r",
                     "read_termination":"\n",}
        self.echo = False
        Driver.__init__(self,spec_test)

    def read_multiple(self):
        val = self.read_instrument("")
        # val = self._to_float(val)
        return val
    
    def read_sens_temp(self):
        val = self.read_instrument(20,1)
        val = self._to_int(val)
        return val

    def read_flow(self):
        val = self.read_instrument(15,1)
        return val

def main():
    inst = LHG3900({})
    x = 19
    while x < 20:
        x+=1
        print(inst.read_multiple())

if __name__ == "__main__":
    main()
