""" weather v0.2
Weather handler for raspi-cloudlamp
"""

# Imports
from datetime import datetime
from mylog import get_logger
import requests

# Constants
DAY = 0
NIGHT = 1


class Weather(object):
    """Class used to retrieve current weather conditions

    Uses the openweathermap.org api: api.openweathermap.org/data/2.5
    """

    def __init__(
        self,
        inet=requests,
        zipcode="97007",
        country="us",
        interval=3600,
        appid=None,
    ):
        """(Weather, requests, str, str, int, str) -> NoneType

        Initializes a weather class object - uses zipcode and country to determine location to get weather for.
        """

        self.log = get_logger(__name__ + ".Weather")
        self.is_active = True
        self.inet = inet
        self.zipcode = zipcode
        self.country = country
        self.appid = appid
        self.id = "def"
        self._raw_response = None
        self.update()
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
            self._zipcode = None
            return

        num_pass = True
        for i in value:
            if i not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                num_pass = False
        if not num_pass:
            self.log.warning(
                f"Zip code must contain numbers only.  Value provided was {str(value)}"
            )
            self._zipcode = None
            return

        self._zipcode = value
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
            self.is_active = False
        self._appid = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def update(self):
        """(Weather, bool) -> bool

        Gets the lastest weather condition and updates the Weather object
        Returns True if the update succeeds and the condition has changed
        """

        self.log.debug("Weather.update() called.")
        if not self.is_active:
            self.log.debug("Updater not active")
            return False

        if self._fetch_update():
            if self._condition_changed():
                return True
            else:
                return False
        else:
            return False

    def _fetch_update(self):
        """Fetches latest update from openweathermaps and stores the resulting JSON in _raw_response
        Returns True on successful fetch, False otherwise"""
        self.log.debug("Calling fetch_update():")
        if self.appid is None:
            self.log.debug("API Key not set!")
            return False

        if self.zipcode is None:
            # Ensure valid zipcode has been set
            self.zipcode = "97007"

        if self.country is None:
            # Ensure valid country has been set
            self.country = "us"

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
            response = self.inet.get(url)
            if response.status_code != 200:
                self.log.warning(
                    f"GET failed with response code: {response.status_code}"
                )
                response.close()
                return False
            self._raw_response = response.json()
            response.close()
            return True
        except (ValueError, RuntimeError) as e:
            self.log.exception(f"Failed to get data:\n {e}")
            return False

    def _condition_changed(self):
        """Returns True if condition ID in self._raw_response is different from currently set self.id
        and sets self.id to new id if so."""
        new_id = self._raw_response["weather"][0]["id"]
        if self.id == new_id:
            self.log.debug(f"Condition id unchanged. Current: {self.id} New: {new_id}")
            return False
        else:
            self.log.debug(f"Condition id changed. Current: {self.id} New: {new_id}")
            self.id = new_id
            return True

    def day_or_night(self):
        sunrise_dt = datetime.fromtimestamp(self._raw_response["sys"]["sunrise"])
        sunset_dt = datetime.fromtimestamp(self._raw_response["sys"]["sunset"])
        now = datetime.now()
        self.log.debug(f"Sunrise: {sunrise_dt} Sunset: {sunset_dt}")

        if not self.is_active:
            self.log.debug("Updater is not active, returning default of DAY")
            return DAY

        if sunrise_dt < now:
            if sunset_dt > now:
                return DAY
            else:
                return NIGHT
        elif sunrise_dt > now:
            return NIGHT
        else:
            return DAY
