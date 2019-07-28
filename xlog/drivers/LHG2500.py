from xlog.drivers.generic_driver_visa_serial import generic_driver_visa_serial as Driver
import logging
import time

logging.basicConfig()
log = logging.getLogger()
# log.setLevel(logging.DEBUG)

class LHG2500(Driver):
    def __init__(self,spec):
        spec_test = {"port": "COM10","baudrate":2400,"write_termination":"\r","read_termination":"\r\n"}
        self.echo = False
        Driver.__init__(self,spec_test)

    def read_multiple(self):
        val = self.read_instrument("?")
        # val = self._to_float(val)
        return val
    
    def read_sens_temp(self):
        val = self.read_instrument(20,1)
        val = self._to_int(val)
        return val

    def read_flow(self):
        val = self.read_instrument(15,1)
        return val

    def set_rh_pc_tc_setpoint(self,args):
        val = self.read_instrument('R2={}'.format(args))
        return val

def main():
    inst = LHG2500({})

    print(inst.read_multiple())

if __name__ == "__main__":
    main()
