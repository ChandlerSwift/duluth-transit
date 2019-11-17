import api_consumer
from .display import strip
from rpi_ws281x import Color
from typing import Tuple
import json
import os

ALL_ROUTE_NUMBERS = ["6", "11", "13", "23"]


class Location(object):
    def __init__(self, lat, long):
        self.lat = lat0
        self.long = long

    @staticmethod
    def distance(pos1, pos2):
        diff_x = pos1.lat - pos2.lat
        diff_y = pos1.long - pos2.long
        return (diff_x**2 + diff_y**2)**0.5


class MapUpdater:

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'routes.json')) as routes_file:
            self.routes = json.loads(routes_file.read())
        self.shown_route_numbers = ALL_ROUTE_NUMBERS # Updated by UI
        # TODO: remove:
        #self.routes = {"13": {"stops": []}}

    def find_nearest_stop(self, route: str, bus_location: Location):
        '''
        Yes, Jeff, this is wrong. I _do_ understand that lines of latitude and
        longitude are not perpendicular, nor square. However, Duluth has quite a
        few other issues like hills, which present much larger discrepancies than
        the curvature of the Earth.

        Plus, the Earth is flat anyway. Wake up, sheeple.
        xkcd.com/{1013,1318}
        '''
        closest_stop = self.routes[route]['stops'][0]
        for route in self.routes:
            for stop in route['stops']:
                if Location.distance(bus_location, stop) < Location.distance(bus_location, closest_stop):
                    closest_stop = stop
        return closest_stop

    def update_map(self):
        # Start as 
        for i in range(strip.numPixels()): # or LED_COUNT
            strip.setPixelColor(i, Color(0,0,0))

        # If we're only showing one map, highlight all the stops
        if len(self.shown_route_numbers) is 1:
            for stop in self.routes[self.shown_route_numbers[0]]['stops']:
                strip.setPixelColor(stop['led'], Color(10,2,2))
            strip.setPixelColor(20, Color(255,255,255))
        else:
            strip.setPixelColor(20, Color(255,10,10))
            strip.setPixelColor(2, Color(10,255,10))
        #for bus in api_consumer.get_buses(shown_routes):
        #    bus_location = Location(bus.lat, bus.long)
        #    show_stop(find_nearest_stop(bus_location))
        strip.show()

    def show_route(self, route: str):
        print("In show_route, previously showing %s" % self.shown_route_numbers)
        self.shown_route_numbers = [route]
        print("Now showing %s" % self.shown_route_numbers)

        self.update_map()

    def show_all_routes(self):
        print("In show_all_routes, previously showing %s" % self.shown_route_numbers)
        self.shown_route_numbers = ALL_ROUTE_NUMBERS
        print("Now showing %s" % self.shown_route_numbers)
        self.update_map()