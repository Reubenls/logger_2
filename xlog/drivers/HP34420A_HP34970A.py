import visa
import time
import numpy as np
import json

class HP34420A_HP34970A(object):
    def __init__(self,spec):
        rm = visa.ResourceManager()
        self.spec = spec
        self.hp420A = rm.open_resource(spec['port_bridge'])
        self.hp970a = rm.open_resource(spec['port_scanner'])

    def read_instrument(self,op_id):
        op = self.spec["operations"][op_id]
        channel = op["channel"]
        nplc = op["nplc"]
        self.configure_nlpc(nplc)
        val = self.read_channel(channel)
        val = np.float64(val)
        val_trans = val
        return val,val_trans

    def read_channel(self,channel):
        self.switch_scanner_channel(channel)
        return self.read()

    def configure_nlpc(self,nplc):
        assert nplc in [0.02, 0.2, 1, 2, 10, 20, 100, 200, 'MIN', 'MAX']
        self.write("VOLT:NPLC {}".format(nplc))

    def read(self):
        return self.hp420A.query("READ?")

    def write(self,arg):
        self.hp420A.write(arg)

    def switch_scanner_channel(self,channel):

        self.hp970a.write("MEAS:VOLT:DC? (@{})".format(channel))
        val = self.hp970a.read()







def main():
    inst = HP34420A_HP34970A(json.load(open('../instruments/HP34420A_HP34970A.json')))
    print(inst.read_instrument('read_px_something'))

if __name__ == '__main__':
   main()



