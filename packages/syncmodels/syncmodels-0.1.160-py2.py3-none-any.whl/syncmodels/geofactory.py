from typing import List, Dict, Any
from geopy import distance
import requests
import re
import json


# from geopy.point import Point
from math import cos, sin, radians, degrees

from agptools.helpers import parse_uri, parse_xuri, build_uri

from .registry import iRegistry
from .model.geofilters import GeoFilterDefinition, GridDefinition
from .model.geojson import Point
from .helpers.geojson import POINT, PointModel

# Madrid: 40.42250610407336, -3.701854740836061
# Finisterre: 42.92579093443574, -9.291690042170146
# Tarifa: 36.003135408268065, -5.610213189770706

# select a point that all coordinates should be positive from this origin?
DEFAULT_CENTER = POINT(
    {
        "lon": -3.7,
        "lat": 40.5,
    }
)
EARTH_RADIUS_KM = 6371.0


class GeoFactory(iRegistry):
    """TBD"""

    CACHE : Dict[str, Dict] = {}
    SOURCES = {
        "airport": "https://raw.githubusercontent.com/jbrooksuk/JSON-Airports/refs/heads/master/airports.json",
    }

    @classmethod
    def get_locator(cls, geo_locator: str,  **context) -> GeoFilterDefinition:
        "(?P<klass>[^_]+)_(?P<>(?P<airport>[^_]+)_(?P<size>\d+)x(\d+))$"

        if not(instance := cls.CACHE.get(geo_locator)):

            def score(item):
                "score by counting how many uri values are not None"
                options, m, d = item
                _uri = parse_xuri(geo_locator)
                sc = 100 * len(m.groups()) + len(
                    [_ for _ in _uri.values() if _ is not None]
                )
                return sc, item

            blue, klass, args, kw = cls.get_factory(geo_locator, __klass__=cls, score=score)
            if klass:
                # find in cache
                uri = parse_uri(geo_locator, **context)
                try:
                    context.update(kw)
                    # more general instance method that class methods
                    factory = klass(*args, **uri, **kw)
                    instance = factory.get_filter(id=geo_locator, **kw)
                    cls.CACHE[geo_locator] = instance
                except Exception as why:  # pragma: nocover
                    print(why)
                    raise

        return instance
    @classmethod
    def get_coordinates(cls, klass: str, uid: str):
        """TODO: generalize"""
        holder = cls.CACHE.setdefault(klass, {})
        if (item := holder.get(uid)) is None:
            url = cls.SOURCES[klass]
            response = requests.get(url)
            universe = response.json()
            pattern = f"{uid}$"
            for item in universe:
                code = item.get("iata") #  TODO: generalize
                if code:
                    if re.match(pattern, code, re.I|re.DOTALL):
                        holder[uid] = item
                        break
        return item


    def __init__(self, *args, **kw):
        "TBD"

    def get_filter(self, *args, **kw):
        raise NotImplementedError()



class GridFractory(GeoFactory):
    """TBD"""
    CENTER_TYPE = "airport"
    def __init__(self, airport: str, size: int, *args, **kw):
        """
        {'airport': 'agp', 'size': '2'}
        """
        super().__init__(*args, **kw)
        self.airport = airport
        self.size = size

    def get_filter(self, *args, **kw):
        """
        result = factory.get_coordinates(klass="airport", uid="agp")

        kw
        {'klass': 'grid', 'airport': 'agp', 'size': '2'}

        result
        {'iata': 'AGP',
         'lon': '-4.489616',
         'iso': 'ES',
         'status': 1,
         'name': None,
         'continent': 'EU',
         'type': 'airport',
         'lat': '36.675182',
         'size': 'large'}

         grid
         {'id': 'grid_agp_2x2',
          'id__': None,
          'updated': None,
          'center': {'type': 'Point', 'coordinates': (-4.49589, 36.6798)},
          'size': 2.0,
          'dx': 0.01804194792686629,
          'dy': 0.01798643211837461}

        """
        call_kw = {
            "klass": self.CENTER_TYPE,
            "uid": kw.get(self.CENTER_TYPE),
            }
        data = self.get_coordinates(**call_kw)
        kw["center"] = Point(coordinates=[data["lon"], data["lat"]])
        grid = GridDefinition(**kw)
        return grid



class Grid:
    "Helper class for grid operations."

    def __init__(self, center: PointModel = DEFAULT_CENTER, grid_size_km=2):
        """grid_size: grid size in Km."""
        self.center = center
        self.x0 = self.center.coordinates.lon
        self.y0 = self.center.coordinates.lat
        self.grid_size_km = grid_size_km
        self.dx = 0
        self.dy = 0
        self.compute_deltas()

    def compute_deltas(self):
        """Computes the grid size in degrees."""
        # Calculate the difference in longitude
        self.dx = degrees(self.grid_size_km / (EARTH_RADIUS_KM * cos(radians(self.y0))))
        self.dy = degrees(self.grid_size_km / EARTH_RADIUS_KM)

    def grid_to_geo(self, grid_point):
        """Converts grid point to geo coordinates."""
        # TODO: implement grid point to geo conversion

    #     def geo_to_grid(self, geo):
    #         """Converts geo coordinates to grid point."""
    #         dx = geo["lon"] - self.center["lon"]
    #         dy = geo["lat"] - self.center["lat"]
    #
    #         # Round to nearest grid point
    #         nx = dx // self.dx
    #         ny = dy // self.dy
    #         return {"nx": nx, "ny": ny}

    def coordinates_to_geokey(self, p: List):
        """Fast conversion from geo coordinates to grid point.
        doesn't check for point
        """
        dx = p[0] - self.x0
        dy = p[1] - self.y0

        # Round to nearest grid point
        nx = int(dx // self.dx)
        ny = int(dy // self.dy)
        return {"nx": nx, "ny": ny}


# -------------------------------------------------------------------
# Self registry
# -------------------------------------------------------------------

GridFractory.register_itself("(?P<klass>grid)_(?P<airport>[^_]+)_(?P<size>\d+)x(\d+)$") # TODO: agp: force match 'size' i.e 2x2
foo = 1
