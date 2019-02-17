import random
import json
import struct
import time


class test_device(object):
    def __init__(self,spec):
        self.spec = spec
        
    def read_instrument(self):
        time.sleep(0.1)
        return 1234.4231

    def read_test(self):
        return self.read_instrument()

    def read(self,op):
        if hasattr(self,op) and callable(getattr(self,op)):
            f = getattr(self,op)
            return f()
        else:
            print ("error _ to fix lookup json ")
            return(-1)

def main():
    pass
    
if __name__ == '__main__':
    main()