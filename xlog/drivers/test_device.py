import random
import json
import struct
import time


class test_device(object):
    lock = None
    def __init__(self,spec):
        self.spec = spec
        self.value = 1
        self.s_pts = {'rh':0,'t':0,'q':0}
        
    def read_instrument(self):
        time.sleep(0.1)
        return self.value

    def read_test(self):
        return self.read_instrument()

    def write_test(self,val):
        self.value = val
        return("set value {}".format(val))

    def set_rh_sp(self,val):
        self.s_pts['rh'] = val
        return self.s_pts.get('rh')

    def read_rh_sp(self):
        return self.s_pts.get('rh','not found')

    def read(self,op):
        if hasattr(self,op) and callable(getattr(self,op)):
            f = getattr(self,op)
            return f()
        else:
            print ("error _ to fix lookup json ")
            return(-1)

    async def request(self,op,args=None):
        if hasattr(self,op) and callable(getattr(self,op)):
            f = getattr(self,op)
            if args is not None:
                return f(*args)
            else:
                return f()
        else:
            print ("error _ to fix lookup json ")
            return(-1)

    def write(self,op,args):
        

        if hasattr(self,op) and callable(getattr(self,op)):
            f = getattr(self,op)
            return f(*args)
        else:
            print ("error _ to fix lookup json ")
            return(-1)



def main():
    pass
    
if __name__ == '__main__':
    main()