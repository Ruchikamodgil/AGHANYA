from pyowm import OWM
key = "d94f854d7176226f1fc9f8d2f2d64fcc"
owm = OWM(key)  # You MUST provide a valid API key
mgr = owm.weather_manager()


observation_list = mgr.weather_around_coords(29.965223,76.887212)
print(observation_list)
for ix in range (len(observation_list)):
    observation = observation_list[ix]
    w = observation.weather
    print(w)  
    print(type(w))                # <Weather - reference time=2013-12-18 09:20, status=Clouds>

    # # Weather details
    print(w.wind())                  # {'speed': 4.6, 'deg': 330}
    print(w.humidity)                # 87
    print(w.temperature('celsius'))  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    print(w.status)
    print(w.detailed)
    