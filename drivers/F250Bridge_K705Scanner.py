import visa
import time
import numpy as np
import json

class F250Bridge_K705Scanner(object):
    def __init__(self,spec):

        self.spec = spec
        rm = visa.ResourceManager()
        self.bridge = rm.open_resource(spec["port_bridge"])
        self.scanner = rm.open_resource(spec["port_scanner"])
        self.active_channel = 13
        self.bridge.read_termination = '\r\n'

    def read_instrument(self,op_id):
        op = self.spec["operations"][op_id]
        channel = op["channel"]
        prt = op["bridge_prt"]
        self.switch_bridge_prt(prt)

        val = self.read_channel(channel)

        print(val)
        val = val[1:-1]
        val  = f = np.float64(val)
        val_trans = val  # TODO add transform equation
        return val,val_trans


    def read_channel(self,channel):
        self.switch_scanner_channel(channel)
        time.sleep(0.5)
        i = 0
        while self.bridge.read_stb() != 65:
            i += 1
            if i > 5:
                break
            time.sleep(0.5)
        return self.read()

    def read(self):
        return self.bridge.read()

    def write(self,arg):
        self.bridge.write(arg)

    def switch_scanner_channel(self,channel):
        assert channel in range(11, 20)
        self.open_all_channels()
        # self.scanner.write("N{}X".format(self.active_channel))
        # SCANNER WAIT TIME NEEDED

        self.scanner.write("B{}X".format(channel))
        self.scanner.write("C{}X".format(channel))
        time.sleep(4)
        self.active_channel = channel



    def open_all_channels(self):
        self.scanner.write("RX")

    def hi_res(self):
        self.bridge.write('R1')

    def unit_ohms(self):
        self.bridge.write('U3')

    def close_channel(self,channel):
        self.write("N{}X".format((channel)))

    def read_scanner_channel(self):
        return self.scanner.query("G0")

    def switch_bridge_prt(self,prt):
        # assert prt in ['A','B','C','D','I','J','K','L']
        self.bridge.write("M{}".format(prt))

def main():
    inst = F250Bridge_K705Scanner(json.load(open('../instruments/F250Bridge_K705Scanner.json')))
    print(inst.read_instrument('read_tx_something'))

if __name__ == '__main__':
    main()



