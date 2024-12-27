#!/usr/bin/env python3
"""
gps conversions

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

import os
import cmath
from math import degrees, radians
from typing import Tuple
from pymap3d import enu2geodetic, geodetic2enu  # type: ignore


GPS_REF: tuple[float, float] | None = None

# get gps reference from environment variable
var = os.environ.get("GPS_REF")

if var is not None:
    GPS_REF = tuple(float(x) for x in var.split(","))  # type: ignore


def set_gps_ref(lat: float, lon: float) -> None:
    """set gps reference point"""
    global GPS_REF  # pylint: disable=global-statement
    GPS_REF = (lat, lon)


def heading_to_theta(angle_deg: float) -> float:
    """convert gps heading to theta in radians"""
    h = -1j * cmath.rect(1, radians(angle_deg))
    return -cmath.phase(h)


def theta_to_heading(angle_rad: float) -> float:
    """convert theta in radians to gps heading"""
    h = -1j * cmath.rect(1, angle_rad)
    return degrees(-cmath.phase(h))  # type: ignore


def latlon_to_enu(latlon: Tuple[float, float]) -> Tuple[float, float]:
    if GPS_REF is None:
        raise EnvironmentError("GPS_REF not set")
    x, y, _ = geodetic2enu(latlon[0], latlon[1], 0, GPS_REF[0], GPS_REF[1], 0)
    return float(x), float(y)


def enu_to_latlon(xy: Tuple[float, float]) -> Tuple[float, float]:
    if GPS_REF is None:
        raise EnvironmentError("GPS_REF not set")
    lat, lon, _ = enu2geodetic(xy[0], xy[1], 0, GPS_REF[0], GPS_REF[1], 0)
    return float(lat), float(lon)


def _nmea_to_decimal_degrees(nmea_coord: str, degrees_index: int) -> float:
    """convert nmea coordinate to decimal degrees"""

    # Split the NMEA coordinate into degrees and minutes
    c_deg = int(nmea_coord[:degrees_index])
    c_min = float(nmea_coord[degrees_index:])

    # Convert to decimal degrees
    decimal_degrees = c_deg + c_min / 60.0

    return decimal_degrees


def parse_nmea_lat(nmea_coord: str) -> float:
    """parse NMEA latitude coordinate"""
    return _nmea_to_decimal_degrees(nmea_coord, 2)


def parse_nmea_lon(nmea_coord: str) -> float:
    """parse NMEA longitude coordinate"""
    return _nmea_to_decimal_degrees(nmea_coord, 3)
