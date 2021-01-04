"""
Remote handler for APCloudLight 2020
"""

# Imports
from evdev import InputDevice, categorize, ecodes
# import adafruit_logging as logging

# Create and setup logger
remlog = logging.getLogger("raspi-cloudlamp.remote")


class IRRemote(object):
    """Class for the IRRemote object

    Use:
        remote = IRRemote(board.PIN, button_mapping)
        remote.enable()
        while True:
            while(not remote.received())
                pass
            if remote.decode():
                print('Decoded signal matching protocol and mapped to mapping')
                print(remote.pressed)
            else:
                print('Unknown or unmapped signal')
            remote.enable()
    """

    def __init__(self, mapping, input_device="/dev/input/event0"):
        """Initialize IRRemote class

        param:pin       The pin for the IR Receiver using board.PIN format
        param:mapping   A dictionary of key:value pairs with the key being
                        the hex code (as a string) for the remote button and
                        the value being the friendly button name
        param:protocol  The protocol that the remote should be using to decode
                        the pulses. Default is NEC
        """

        self.log = logging.getLogger("raspi-cloudlamp.remote.IRRemote")
        self.log.setLevel(logging.INFO)
        self._event = None
        self.pressed = None
        self.mapping = mapping
        self._device = InputDevice(input_device)
        self.log.info("Created instance of IRRemote Class.")

    @property
    def pressed(self):
        """ Returns the name of the key pressed as a string based on the provided mapping """
        return self._pressed

    @pressed.setter
    def pressed(self, value):
        self._pressed = value

    # Class functions
    def received(self):
        """ Checks to see if a remote button press was recieved and returns True if so """
        evt = self._device.read_one()
        while evt != None:
            if evt.type != ecodes.EV_KEY:
                evt = self._device.read_one()
                continue
            event = str(categorize(evt))
            self.log.debug(f"Recieved valid event: {event}")
            if "up" in event[-2:]:
                self.pressed = self.mapping[
                    event.split()[5].strip(",").strip("(").strip(")")
                ]
                return True

            evt = self._device.read_one()

        return False

    def close(self):
        self._device.close()
        self.log.info("Closed connection to IR device.")
