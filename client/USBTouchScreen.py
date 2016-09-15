# USBKeyboard.py
#
# Contains class definitions to implement a USB keyboard.

from USB import *
from USBDevice import *
from USBConfiguration import *
from USBInterface import *
from USBEndpoint import *
import curses

class USBTouchScreenInterface(USBInterface):
    name = "USB TouchScreen interface"

    hid_descriptor = b'\x09\x21\x10\x01\x00\x01\x22\x2b\x00'
    report_descriptor = b"""
    \x05\x0D
    \x09\x04
    \xA1\x01

    \x09\x55
    \x25\x01
    \xB1\x02

    \x09\x54
    \x95\x01
    \x75\x08
    \x81\x02

    \x09\x22
    \xA1\x02

    \x09\x51
    \x75\x08
    \x95\x01
    \x81\x02

    \x09\x42
    \x09\x32
    \x15\x00
    \x25\x01
    \x75\x01
    \x95\x02
    \x81\x02

    \x95\x06
    \x81\x03

    \x05\x01
    \x09\x30
    \x09\x31
    \x16\x00\x00
    \x26\x10\x27
    \x36\x00\x00
    \x46\x10\x27
    \x66\x00\x00
    \x75\x10
    \x95\x02
    \x81\x02
    \xC0
    \xC0"""

    def __init__(self, verbose=0):
        descriptors = {
                USB.desc_type_hid    : self.hid_descriptor,
                USB.desc_type_report : self.report_descriptor
        }

        self.endpoint = USBEndpoint(
                3,          # endpoint number
                USBEndpoint.direction_in,
                USBEndpoint.transfer_type_interrupt,
                USBEndpoint.sync_type_none,
                USBEndpoint.usage_type_data,
                16384,      # max packet size
                10,         # polling interval, see USB 2.0 spec Table 9-13
                self.handle_buffer_available    # handler function
        )

        # TODO: un-hardcode string index (last arg before "verbose")
        USBInterface.__init__(
                self,
                0,          # interface number
                0,          # alternate setting
                3,          # interface class
                0,          # subclass
                0,          # protocol
                0,          # string index
                verbose,
                [ self.endpoint ],
                descriptors
        )

        self.keys = [ ]

    def handle_buffer_available(self):
        if not self.keys:
            return

        data = self.keys.pop(0)
        self.endpoint.send(data)


class USBTouchScreenDevice(USBDevice):
    name = "USB keyboard device"

    def __init__(self, maxusb_app, verbose=0):
        config = USBConfiguration(
                1,                                          # index
                "Emulated TouchScreen",    # string desc
                [ USBTouchScreenInterface() ]                  # interfaces
        )

        USBDevice.__init__(
                self,
                maxusb_app,
                0,                      # device class
                0,                      # device subclass
                0,                      # protocol release number
                64,                     # max packet size for endpoint 0
                0x04e7,                 # vendor id
                0x0030,                 # product id
                0x1234,                 # device revision
                "manufacture",          # manufacturer string
                "product",              # product string
                "S/N12345",             # serial number string
                [ config ],
                verbose=verbose
        )

