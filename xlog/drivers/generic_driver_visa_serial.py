import visa
import json
import time
from decimal import Decimal

class generic_driver_visa_serial(object):

    def __init__(self, spec):
        self.spec = spec
        port = spec["port"]
        baud = spec["baudrate"]
        w_term = spec.get("write_termination",'\r')
        r_term = spec.get("read_termination",'\r\n')
        rm = visa.ResourceManager()
        self.store = {}
        self.timeout = spec.get("store_timeout",2)
        self.instrument = rm.open_resource(port,
                                           baud_rate=baud,
                                           write_termination=w_term,
                                           read_termination=r_term)
        self.instrument.open()

    def read_instrument(self,query):

        data = self.instrument.query(query)
        if self.echo == True:
            data = self.instrument.read()
        return data

    #todo writing to instruments
    def write_instrument(self,operation_id,values):
            """
            write instrument 
            """
            #todo: check valid values for sending to instrument
            op = self.operations[operation_id]
            command = op.get("command","")
            print(self.instrument.timeout)
            command = command.format(*values)

            response = self.instrument.query(command)
            #response = self.instrument.read()
            print(response) #todo check response for errors
            return response

    def action_instrument(self,operation_id):
        with self.lock:
            self.instrument.timeout = 10000
            op = self.operations[operation_id]
            command = op.get("command","")
            response = self.instrument.query(command,delay=1)
            self.timeout = 2000
            print(response)  # todo check response for errors
            return response

    def decimals(self,data,operation):
        d_shift = operation.get('decimal_shift',0)
        d = Decimal(data).scaleb(d_shift)
        # f = np.float64(d)
        return d

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

#testing
def main():
    instr = generic_driver_visa_serial(json.load(open('../instruments/Vaisala_HMT337.json')))
    print(instr.read_instrument('read_default'))
    print(instr.read_instrument('read_rh'))
    # print (instr.action_instrument('action_generate'))
    #print (instr.write_instrument('set_dew_point_setpoint',[5.00]))
    # time.sleep(2)
    # print (instr.read_instrument('read_setpoints'))
    # print (instr.action_instrument('action_stop'))

if __name__ == '__main__':
    main()