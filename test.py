import bluepy.btle
from bluepy.btle import Peripheral
import time

def try_until_success(func, exception=bluepy.btle.BTLEException, msg='reattempting', args=[]):
    retry = True
    while True:
        try:
            func(*args)
            retry = False
        except exception:
            print msg

        if not retry:
            break

BT_MAC = '00:2A:40:08:00:10'
CMD_TURN_ON = 'ledonledonledonledon'
CMD_TURN_OFF = 'ledoffledoffledoffle'

hexi = Peripheral()

try_until_success(hexi.connect, msg='error connect', args=[BT_MAC])

ledctl = hexi.getCharacteristics(uuid='2031')[0] # Alert Input

for i in range(10):
    try_until_success(ledctl.write, msg='error turn on', args=[CMD_TURN_ON, True])
    time.sleep(2)
    try_until_success(ledctl.write, msg='error turn off', args=[CMD_TURN_OFF, True])
    time.sleep(2)
