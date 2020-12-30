'''
Weather handler for APCloudLight 2020
'''

# Imports
import time
from mysecrets import secrets
import adafruit_logging as logging
import requests

wthlog = logging.getLogger('cloud.weather')

class Weather(object):
    """ Class used to retrieve current weather conditions
    
    Uses the openweathermap.org api: api.openweathermap.org/data/2.5
    """
    
    def __init__(self, wifi=requests, zipcode = '97007', country = 'us', interval = 3600, appid = secrets['ow_appid']):
        """ (Weather, Wifi, str, str, int, str) -> NoneType
        
        Initializes a weather class object - uses zipcode and country to determine location to get weather for.
        """
        
        self.log = logging.getLogger('cloud.weather.Weather')
        self.log.setLevel(logging.INFO)
        self.log.info('Creating instance of Weather Class.')
        self.is_active = False
        self.wifi = wifi # adafruit wifimanager object
        self.zipcode = zipcode
        self.country = country
        self.appid = appid
        self.current = 'Undefined'
        self.id = 'Undefined'
        self.interval = interval
        self._next_update = time.monotonic()
        self.update(True)
    
    @property
    def zipcode(self):
        """ (Weather) -> str
        
        Returns the zipcode for the Weather object as a string
        """
        
        return str(self._zipcode)
    
    @zipcode.setter
    def zipcode(self, value):
        """ (Weather, str) -> NoneType
        
        Sets the self._zipcode variable of the Weather object to the provided value
        """
        
        self.log.debug('Setting zip code')
        if len(value) != 5:
            self.log.warning(f'Zip code must be 5 characters.  Value provided was {str(value)}')
            return
    
        for i in value:
            if i not in ['0','1','2','3','4','5','6','7','8','9']:
                self.log.warning(f'Zip code must contain numbers only.  Value provided was {str(value)}')
                return
        
        self._zipcode = value
        self.is_active = True
        self.log.debug(f'Zip code set: {self._zipcode}')
    
    @property
    def country(self):
        """ (Weather) -> str
        
        Returns the country for the Weather object as a string
        """
        
        return str(self._country)
    
    @country.setter
    def country(self, value):
        """ (Weather, str) -> NoneType
        
        Sets the self._country variable of the Weather object to the provided value
        """
        
        # Need some value checking code here
        self.log.debug(f'Setting country: {value}') 
        self._country = value
    
    @property
    def appid(self):
        """ (Weather) -> str
        
        Returns the appid for the Weather object as a string
        """
        
        return str(self._appid)
    
    @appid.setter
    def appid(self, value):
        """ (Weather, str) -> NoneType
        
        Sets the self._appid variable of the Weather object to the provided value
        """
        
        # Need some value checking code here
        self.log.debug(f'Setting appid: {value}')
        self._appid = value
        
    @property
    def current(self):
        """ (Weather) -> str
        
        Returns the current condition for the Weather object as a string
        """
        
        return str(self._current)
    
    @current.setter
    def current(self, value):
        """ (Weather, str) -> NoneType
        
        Sets the self._current variable of the Weather object to the provided value
        """
        
        # Need some value checking code here
        self.log.debug(f'Setting current condition: {value}')
        self._current = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def update(self, force=False):
        """ (Weather) -> NoneType
        
        Gets the lastest weather condition and updates the Weather object
        Returns True if the update succeeds and the condition has changed
        """
        
        self.log.debug('Calling Weather.update() - before time check')
        now = time.monotonic()
        if now < self._next_update and not force:
            return False
        
        self.log.info('Calling Weather.update() - enough time has passed')
        
        url = 'https://api.openweathermap.org/data/2.5/weather?units=imperial&zip=' + self.zipcode + ',' + self.country + '&appid=' + self.appid
        
        try:
            self.log.debug('Attempting to get response . . .')
            response = self.wifi.get(url)
            if response.status_code != 200:
                self.log.warning(f'GET Failed with response code: {response.status_code}')
                response.close()
                self._next_update = now + 600  #Try again in 10 minutes
                return False
            resp = response.json()
            response.close()
        except (ValueError, RuntimeError) as e:
            self.log.exception(f'Failed to get data:\n {e}')
            #self.wifi.reset()
            self._next_update = now + 600 #Try again in 10 minutes
            return False
        
        new_condition = resp['weather'][0]['main']
        new_id = resp['weather'][0]['id']
        self.log.info(f'Retrieved weather condition update: {new_condition}')
        if self.id == new_id:
            # No Change, we'll try again in another self.interval
            self.log.info(f'Condition unchanged. Current: {self.id},{self.current} New: {new_id},{new_condition}')
            self._next_update = now + self.interval
            return False
        else:
            # Condition changed, let's update it and return True
            self.log.info(f'Condition changed: Current: {self.id},{self.current} New: {new_id},{new_condition}')
            self.current = new_condition
            self.id = new_id
            self._next_update = now + self.interval
            return True
        
        self.log.critical('Weather.update() got to the end without returning')
        self._next_update = now + self.interval
        return False
