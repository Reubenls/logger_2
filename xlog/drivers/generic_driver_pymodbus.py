from pymodbus.client.sync import ModbusSerialClient as ModbusClient

import json
import struct
import time


class generic_driver_pymodbus(ModbusClient):
    def __init__(self,spec):
        self.spec = spec
        self.address = spec['address']
        ModbusClient.__init__(self,method='rtu', port=spec['port'],stopbits=spec['stopbits'], baudrate=spec['baudrate'])
        self.connect()
        time.sleep(0.5)

    def read_instrument(self,reg,num_reg=1):
        response = self.read_holding_registers(reg, count=num_reg, unit=self.address)
        if response.isError():
            self.close()
            print (response.message)
            return None
        data = response.registers
        # data = response
        print (data)
        # self.close()
        return data

    def read(self,op):
        if hasattr(self,op) and callable(getattr(self,op)):
            f = getattr(self,op)
            return f()
        else:
            print ("error _ to fix lookup json ")
            return(-1)

    # def decimals(self,data,operation):
    #     d_shift = operation.get('decimal_shift',0)
    #     d =  Decimal(data).scaleb(d_shift)
    #     f = np.float64(d)
    #     return f

    # def transform(self,data,operation):
    #     x = data
    #     eq = operation.get("transform_eq",'x')
    #     c = operation.get("transform_coeff",None)
    #     result = eval(eq)
    #     return result


    # def uint_conversion(self, datatype):
    #     dt = datatype.lower()
    #     if dt == "float":
    #         return self.uint_to_float
    #     elif dt == "int":
    #         return self.uint_to_int
    #     elif dt == "uint":
    #         return self.uint_to_uint
    #     else:
    #         return self.to_uint

    # def uint_to_float(self, data):
    #     mp = struct.pack('!HH', data[1], data[0])
    #     return struct.unpack('!f', mp)[0]

    def _to_int(self, data):
        mp = struct.pack('!H', data[0])
        return struct.unpack('!h', mp)[0]
   
    def _to_float(self, data):
        mp = struct.pack('!HH', data[1], data[0])
        return struct.unpack('!f', mp)[0]


    # def uint_to_uint(self, data):
    #     return data[0]

    # def to_uint(self, data):
    #     return data

#testing
def main():
    instr = generic_driver_pymodbus(json.load(open('instruments/Vaisala_HMP7_modbus.json')))

    print(instr.read_instrument('read_rh'))
    print(instr.read_instrument('read_dew_point_temp'))



if __name__ == '__main__':
    main()