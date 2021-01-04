# Map openweathermap condition codes to weather animations
weather_animations = {
    "200": cloud100,        # T-Storm - light rain
    "201": cloud100,        # T-Storm - rain
    "202": cloud100,        # T-Storm - heavy rain
    "210": cloud100,        # Light T-Storm
    "211": cloud100,        # T-Storm
    "212": cloud100,        # Heavy T-Storm
    "221": cloud100,        # Ragged T-Storm
    "230": cloud100,        # T-Storm - light drizzle
    "231": cloud100,        # T-Storm - drizzle
    "232": cloud100,        # T-Storm - heavy drizzle
    "300": rainlight,       # Light drizzle
    "301": rainlight,       # Drizzle
    "302": rainheavy,       # Heavy drizzle
    "310": rainlight,       # Light drizzle rain
    "311": rainheavy,       # Drizzle rain
    "312": rainheavy,       # Heavy drizzle rain
    "313": rainheavy,       # Shower rain and drizzle
    "314": rainheavy,       # Heavy shower rain and drizzle
    "321": rainheavy,       # Shower drizzle
    "500": rainlight,       # Light rain
    "501": rainlight,       # Moderate rain
    "502": rainheavy,       # Heavy rain
    "503": rainveryheavy,   # Very heavy rain
    "504": rainveryheavy,   # Extreme rain
    "511": rainheavy,       # Freezing rain
    "520": rainlight,       # Light shower rain
    "521": rainheavy,       # Shower rain
    "522": rainheavy,       # Heavy shower rain
    "531": rainveryheavy,   # Ragged shower rain
    "600": snowlight,       # Light snow
    "601": snowheavy,       # Snow
    "602": snowveryheavy,   # Heavy snow
    "611": rainlight,       # Sleet
    "612": rainlight,       # Light shower sleet
    "613": rainheavy,       # Shower sleet
    "615": rainlight,       # Light rain and snow
    "616": rainlight,       # Rain and snow
    "620": snowlight,       # Light shower snow
    "621": snowheavy,       # Shower snow
    "622": snowveryheavy,   # Heavy shower snow
    "701": cloud100,        # Mist
    "711": cloud100,        # Smoke
    "721": cloud100,        # Haze
    "731": cloud100,        # Dust whirls
    "741": cloud100,        # Fog
    "751": cloud100,        # Sand
    "761": cloud100,        # Dust
    "762": cloud100,        # Volcanic Ash
    "771": cloud100,        # Squalls
    "781": cloud100,        # Tornado
    "800": clearday,        # Clear sky
    "801": cloud25,         # Few clouds
    "802": cloud50,         # Scattered clouds
    "803": cloud75,         # Broken clouds
    "804": cloud100,        # Overcast clouds
}