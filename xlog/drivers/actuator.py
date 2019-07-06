import usb.core
import time

CONTROL_COMMANDS = {'SET_ACCURACY': 0x01,
                    'SET_RETRACT_LIMIT': 0x02,
                    'SET_EXTEND_LIMIT': 0x03,
                    'SET_MOVEMENT_THRESHOLD': 0x04,
                    'SET_STALL_TIME': 0x05,
                    'SET_PWM_THRESHOLD': 0x06,
                    'SET_DERIVATIVE_THRESHOLD': 0x07,
                    'SET_DERIVATIVE_MAXIMUM': 0x08,
                    'SET_DERIVATIVE_MINIMUM': 0x09,
                    'SET_PWM_MAXIMUM': 0x0A,
                    'SET_PWM_MINIMUM': 0x0B,
                    'SET_PROPORTIONAL_GAIN': 0x0C,
                    'SET_DERIVATIVE_GAIN': 0x0D,
                    'SET_AVERAGE_RC': 0x0E,
                    'SET_AVERAGE_ADC': 0x0F,
                    'GET_FEEDBACK': 0x10,
                    'SET_POSITION': 0x20,
                    'SET_SPEED': 0x21,
                    'DISABLE_MANUAL': 0x30,
                    'RESET': 0xFF}


def split(i):
    """ Split inteerger into high byte and low byte"""
    i = int(i)
    low = i & 0xff
    high = (i >> 8) & 0xff
    return [low, high]


def join(low, high):
    """ Join high byte and low byte """
    i = (((high & 0xff) << 8) | low)
    return i


class Actuator(object):

    def __init__(self):
        self.writeEP = 0x01
        self.readEP = 0x81
        self.timeout = 500
        self.readlen = 3
        self.extend_Limit = 1014
        self.retract_Limit = 10

    def open(self):
        self.device = usb.core.find(idVendor=0x04d8, idProduct=0xfc5f)
        if self.device is None:
            raise ValueError('device not connected')

        self.device.set_configuration()

    def write(self, control, low, high):
        packet = bytearray([control, low, high])
        self.device.write(self.writeEP, packet, self.timeout)

    def read(self):
        msg = bytearray(3)
        msg = self.device.read(self.readEP, 3, self.timeout)
        return msg

    def set_Extend_Limit(self, position):
        if position < self.retract_Limit or position > 1023 or position < 0:
            print('Position invalid')
            raise ValueError('limit out side of acceptible range')
        command = 0x03
        self.write(command, *split(position))
        response = self.read()
        self.extend_Limit = position
        print('Extend Limit set to '+(str)(self.extend_Limit))

    def set_Retract_Limit(self, position):
        if position > self.extend_Limit or position > 1023 or position < 0:
            print('Position invalid')
            raise ValueError('limit out side of acceptible range')
        command = 0x02
        self.write(command, *split(position))
        response = self.read()
        self.retract_Limit = position
        print('retract Limit set to {}'.format(self.retract_Limit))

    def set_Position(self, percentage):

        if percentage > 100 or percentage < 0:
            print('Position invalid')
            raise ValueError('percentage between 0 and 100 required')

        position = (self.extend_Limit - self.retract_Limit) * (percentage/100)
        position = self.retract_Limit + position
        command = 0x20
        hl = split(position)
        self.write(command, hl[0], hl[1])
        response = self.read()
        print(response)
        self.setPosition = position
        self.setPercentage = percentage
        current_Position = join(response[1], response[2])
        print('position set to {} or {}%'.format(self.setPosition,
                                                 self.setPercentage))

    def set_Position_Override(self, position):
        if position > 1023 or position < 0:
            print('Position invalid')
            raise ValueError('position between 0 and 1023 required')

        command = 0x20
        hl = split(position)
        self.write(command, hl[0], hl[1])
        response = self.read()
        self.setPosition = position
        current_Position = join(response[1], response[2])
        print('position set to {}'.format(self.setPosition))

    def get_Feedback(self):
        command = 0x10
        self.write(command, 0, 0)
        response = self.read()
        print (response)
        position = join(response[1], response[2])
        percentage = ((position - self.retract_Limit) /
                      (self.extend_Limit - self.retract_Limit))*100
        print('Actuator Current Position is {} or {:.2f}%'.format(position,
                                                              percentage))
        return (percentage)

    def set_Accuracy(self, accuracy):
        if accuracy > 10 or accuracy < 0:
            print('accuracy invalid')
            raise ValueError('position between 0 and 1023 required')

        self.write(0x01, accuracy, 0)
        print (self.read())

    def set_Speed(self, speed):
        if speed > 1023 or speed < 0:
            print('speed invalid')
            raise ValueError('position between 0 and 1023 required')

        self.write(0x21, *split(speed))
        print (self.read())


def main():
    dev = Actuator()
    dev.open()
    #dev.get_Feedback()
    #print(dev.read())
    #dev.write(0x21, 255, 3)
    dev.set_Speed(1023)
    #print (dev.read())
    #dev.set_Retract_Limit(20)
    #dev.set_Position(100)
    dev.set_Position_Override(10)
    #dev.write(0x01, 2, 0)
    dev.get_Feedback()

if __name__ == '__main__':
    main()
