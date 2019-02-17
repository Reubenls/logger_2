import asyncio
from pymodbus.client.asynchronous.serial import AsyncModbusSerialClient as ModbusClient
from pymodbus.client.asynchronous.serial import AsyncModbusSerialClient as ModbusClient
from pymodbus.client.asynchronous import schedulers
from decimal import Decimal
import numpy as np
import json
import struct
import time
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class generic_driver_pymodbus(object):
    lock = asyncio.Lock()
    def __init__(self,spec):
        self.spec = spec
        self.address = spec['address']
        # self.operations = spec['operations']
        # ModbusClient.__init__(self,method='rtu', port=spec['port'],stopbits=spec['stopbits'], baudrate=spec['baudrate'])
        print("1")
        try:
            print("2")
            
            self.loop , self.client = ModbusClient("async_io", port=spec['port'],stopbits=spec['stopbits'], baudrate=spec['baudrate'], method="rtu")
            
        except Exception as e:
            print(e)
        print("1")

    async def read_instrument(self,reg,num_reg=1):
        async with lock:

            response =  await self.client.protocol.read_holding_registers(reg, count=num_reg, unit=self.address)
            print(response)

            data = response.registers
            print(data)
            return data

        # except Exception as e:
        #     log.exception(e)
    # async def read_holding_registers(self,reg,num_reg=1):
    #     response =  await self.client.protocol.read_holding_registers(reg, count=num_reg, unit=self.address)
    #     response
    #     print (response)

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

    def _to_float(self, data):
        mp = struct.pack('!HH', data[1], data[0])
        return struct.unpack('!f', mp)[0]

    def _to_int(self, data):
        mp = struct.pack('!H', data[0])
        return struct.unpack('!h', mp)[0]

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