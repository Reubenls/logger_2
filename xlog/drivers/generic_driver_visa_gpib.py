import visa
import json
import time
from decimal import Decimal

class generic_driver_visa_gpib(object):

    def __init__(self,spec):
        self.spec = spec
        # self.operations = spec['operations']
        #self.operations =[ ]
        port = spec["port"]
        # baud = spec["baudrate"]
        # w_term = spec["write_termination"]
        # r_term = spec["read_termination"]
        rm = visa.ResourceManager()
        # self.store = {}
        # self.timeout = 2
        self.instrument = rm.open_resource(address)
        #self.instrument.open() is needed?

    def read_instrument(self,command):
        """
        read instrument 
        """
        return self.instrument.q

        return data, data_trans

    def query(self,request):
        return self.instrument.query(request)

    def write(self):
        pass
    #todo writing to instruments
    def write_instrument(self,operation_id,values):
        """
        write instrument 
        """
        return "not working yet"

    def decimals(self,data,operation):
        d_shift = operation.get('decimal_shift',0)
        return Decimal(data).scaleb(d_shift)

    def transform(self,data,operation):
        x = data
        eq = operation.get("transform_eq",'x')
        c = operation.get("transform_coeff",None)
        result = eval(eq)
        return result

    def convert_to(self,data,datatype):
        if datatype == 'int':
            return int(data)
        elif datatype == 'float':
            return float(data)
        else:
            return data

# #testing
# def main():
#     instr = generic_driver_visa(json.load(open('../instruments/LHG3900_visa.json')))
#     print (instr.read_instrument('read_default'))
#     print (instr.read_instrument('read_default'))
#     time.sleep(2)
#     print (instr.read_instrument('read_default'))
#
#
# if __name__ == '__main__':
#     main()