"""
Remote handler for APCloudLight 2020
"""

# Imports
from evdev import InputDevice
import adafruit_logging as logging

# Create and setup logger
remlog = logging.getLogger("cloud.remote")


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

        self.log = logging.getLogger("cloud.remote.IRRemote")
        self.log.setLevel(logging.INFO)
        self.log.info("Creating instance of IRRemote Class.")
        self._event = None
        self.pressed = None
        self.mapping = mapping
        self._device = InputDevice(input_device)

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
        self.log.debug("Calling received()")
        try:
            self._event = next(self._device.read())
            self.pressed = self.mapping[hex(self._event.value)]
        except (BlockingIOError, KeyError):
            return False
        return True

    def close(self):
        self._device.close()
