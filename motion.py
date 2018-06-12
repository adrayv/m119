from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate, ScanEntry, Peripheral
import struct

# mode determines which data to expect in the next reading
ID_X = 120
ID_Y = 121
ID_Z = 122

mode = None
x = 0
y = 0
z = 0

# This is a delegate for receiving BTLE events
class BTEventHandler(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
    	# Advertisement Data
        if isNewDev:
            print "Found new device:", dev.addr, dev.getScanData()

        # Scan Response
        if isNewData:
            print "Received more data", dev.addr, dev.getScanData()

    def handleNotification(self, cHandle, data):
    	# Only print the value when the handle is 40 (the battery characteristic)
        if cHandle == 40:
            global mode, ID_X, ID_Y, ID_Z, x, y, z
            reading = struct.unpack('B', data)[0]

            # if reading is either x, y, or z then decide the mode based on the reading
            if(reading >= ID_X and reading <= ID_Z):
                mode = reading

            # so if its not less than x,y,z and its valid reading (<= 100), then assign reading based on mode
            elif(reading <= 100):
                if(mode == ID_X):
                    x = reading
                elif(mode == ID_Y):
                    y = reading
                elif(mode == ID_Z):
                    z = reading
                    print('X', x, 'Y:', y, 'Z:', z)
            
handler = BTEventHandler()

# Create a scanner with the handler as delegate
scanner = Scanner().withDelegate(handler)

# Start scanning. While scanning, handleDiscovery will be called whenever a new device or new data is found
devs = scanner.scan(10.0)

# Get HEXIWEAR's address
hexi_addr = [dev for dev in devs if dev.getValueText(0x8) == 'HEXIWEAR'][0].addr
# hexi_addr = '00:2A:40:08:00:10'

# Create a Peripheral object with the delegate
hexi = Peripheral().withDelegate(handler)

# Connect to Hexiwear
hexi.connect(hexi_addr)

# Get the battery service
battery = hexi.getCharacteristics(uuid="2a19")[0]
# battery = hexi.getCharacteristics(uuid="2001")[0]

# Get the client configuration descriptor and write 1 to it to enable notification
battery_desc = battery.getDescriptors(forUUID=0x2902)[0]
# battery_desc = battery.getDescriptors(forUUID=0x2001)[0]
battery_desc.write(b"\x01", True)

# Infinite loop to receive notifications
while True:
    hexi.waitForNotifications(1.0)
