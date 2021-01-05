"""
Weather handler for raspi-cloudlamp
Module ver: v0.1
"""

# Imports
import time
from mylog import get_logger
import requests


class Weather(object):
    """Class used to retrieve current weather conditions

    Uses the openweathermap.org api: api.openweathermap.org/data/2.5
    """

    def __init__(
        self,
        wifi=requests,
        zipcode="97007",
        country="us",
        interval=3600,
        appid=None,
    ):
        """(Weather, Wifi, str, str, int, str) -> NoneType

        Initializes a weather class object - uses zipcode and country to determine location to get weather for.
        """

        self.log = get_logger(__name__ + ".Weather")
        self.is_active = False
        self.wifi = wifi  # adafruit wifimanager object
        self.zipcode = zipcode
        self.country = country
        self.appid = appid
        self.current = "Undefined"
        self.id = "Undefined"
        self.interval = interval
        self._next_update = time.monotonic()
        self.update(True)
        self.log.info("Instance of Weather class created.")

    @property
    def zipcode(self):
        """(Weather) -> str

        Returns the zipcode for the Weather object as a string
        """

        return self._zipcode

    @zipcode.setter
    def zipcode(self, value):
        """(Weather, str) -> NoneType

        Sets the self._zipcode variable of the Weather object to the provided value
        """

        self.log.info("Setting zip code . . .")
        if len(value) != 5:
            self.log.warning(
                f"Zip code must be 5 characters.  Value provided was {str(value)}"
            )
            return

        for i in value:
            if i not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                self.log.warning(
                    f"Zip code must contain numbers only.  Value provided was {str(value)}"
                )
                return

        self._zipcode = value
        self.is_active = True
        self.log.info(f"Zip code set: {self._zipcode}")

    @property
    def country(self):
        """(Weather) -> str

        Returns the country for the Weather object as a string
        """

        return self._country

    @country.setter
    def country(self, value):
        """(Weather, str) -> NoneType

        Sets the self._country variable of the Weather object to the provided value
        """

        # Need some value checking code here
        self.log.info(f"Setting country: {value}")
        self._country = value

    @property
    def appid(self):
        """(Weather) -> str

        Returns the appid for the Weather object as a string
        """

        return self._appid

    @appid.setter
    def appid(self, value):
        """(Weather, str) -> NoneType

        Sets the self._appid variable of the Weather object to the provided value
        """

        self.log.info(f"Setting appid: {value}")
        if value is None:
            self.log.warning("No API Key provided")
        self._appid = value

    @property
    def current(self):
        """(Weather) -> str

        Returns the current condition for the Weather object as a string
        """

        return self._current

    @current.setter
    def current(self, value):
        """(Weather, str) -> NoneType

        Sets the self._current variable of the Weather object to the provided value
        """

        # Need some value checking code here
        self.log.debug(f"Setting current condition: {value}")
        self._current = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def update(self, force=False):
        """(Weather) -> NoneType

        Gets the lastest weather condition and updates the Weather object
        Returns True if the update succeeds and the condition has changed
        """

        self.log.debug("Calling Weather.update() - before time check")
        now = time.monotonic()
        if (now < self._next_update or self.appid is None) and not force:
            return False

        self.log.debug("Calling Weather.update() - enough time has passed")

        if self.appid is None:
            self.log.warning("API Key not set - defaulting to clear condition")
            self.current = "Clear"
            self.id = "800"
            self._next_update = now + self.interval
            return False

        url = (
            "https://api.openweathermap.org/data/2.5/weather?units=imperial&zip="
            + self.zipcode
            + ","
            + self.country
            + "&appid="
            + self.appid
        )

        try:
            self.log.debug("Attempting to get response . . .")
            response = self.wifi.get(url)
            if response.status_code != 200:
                self.log.warning(
                    f"GET Failed with response code: {response.status_code}"
                )
                response.close()
                self._next_update = now + 600  # Try again in 10 minutes
                return False
            resp = response.json()
            response.close()
        except (ValueError, RuntimeError) as e:
            self.log.exception(f"Failed to get data:\n {e}")
            # self.wifi.reset()
            self._next_update = now + 600  # Try again in 10 minutes
            return False

        new_condition = resp["weather"][0]["main"]
        new_id = resp["weather"][0]["id"]
        self.log.debug(f"Retrieved weather condition update: {new_condition}")
        if self.id == new_id:
            # No Change, we'll try again in another self.interval
            self.log.debug(
                f"Condition unchanged. Current: {self.id},{self.current} New: {new_id},{new_condition}"
            )
            self._next_update = now + self.interval
            return False
        else:
            # Condition changed, let's update it and return True
            self.log.info(
                f"Condition changed: Current: {self.id},{self.current} New: {new_id},{new_condition}"
            )
            self.current = new_condition
            self.id = new_id
            self._next_update = now + self.interval
            return True

        self.log.critical("Weather.update() got to the end without returning")
        self._next_update = now + self.interval
        return False
