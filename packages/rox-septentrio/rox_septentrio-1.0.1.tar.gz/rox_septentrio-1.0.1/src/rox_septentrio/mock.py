#!/usr/bin/env python3
"""
 Mock gps functions and classes

 Copyright (c) 2023-2024 ROX Automation - Jev Kuznetsov

fix types:
    0 = Invalid, no position available.
    1 = Autonomous GPS fix, no correction data used.
    2 = DGPS fix, using a local DGPS base station or correction service, such as WAAS.
    3 = PPS fix, never used?.
    4 = RTK fix, high accuracy Real Time Kinematic.
    5 = RTK Float, better than DGPS, but not quite RTK.
    6 = Estimated fix (dead reckoning).
    7 = Manual input mode.
    8 = Simulation mode.
    9 = WAAS fix (not NMEA standard, but NovAtel receivers report this instead of a 2).

"""
import asyncio
import logging
import math
import operator
from collections import OrderedDict
from datetime import datetime
from functools import reduce
from typing import NamedTuple, Tuple
from rox_septentrio.runners import run_main_async

from rox_septentrio.converters import (enu_to_latlon, heading_to_theta,
                                       latlon_to_enu, theta_to_heading, GPS_REF)

log = logging.getLogger("mock_gps")


def sd_to_dm(latitude: float, longitude: float) -> Tuple[str, str, str, str]:
    """convert decimals to DDDMM.SSSS format and their directions"""

    if latitude < 0:
        lat_dir = "S"
    else:
        lat_dir = "N"
    lat = f"{abs(int(latitude)) * 100 + (abs(latitude) % 1.0) * 60:010.5f}".rstrip(
        "0"
    )

    if longitude < 0:
        lon_dir = "W"
    else:
        lon_dir = "E"
    lon = (
        f"{abs(int(longitude)) * 100 + (abs(longitude) % 1.0) * 60:011.5f}"
    ).rstrip("0")

    return lat, lat_dir, lon, lon_dir


def nmea_msg(sentence: str) -> str:
    """add starting $ and checksum to a message"""
    checksum = reduce(operator.xor, map(ord, sentence), 0)
    return f"${sentence}*{checksum:02x}"


class NMEA_Message:
    """nmea message generator"""

    def __init__(self, sentence_type: str, fields: OrderedDict) -> None:
        self.sentence_type = sentence_type
        self.fields = fields

    def __str__(self) -> str:
        sentence = f"{self.sentence_type},{','.join(self.fields.values())}"
        return nmea_msg(sentence)

    def get(self, name: str) -> str:
        """get field value"""
        return self.fields[name]

    def set(self, name: str, val: str) -> None:
        """set field value"""
        self.fields[name] = val

    def timestamp_now(self) -> None:
        """set timestamp to current time"""
        self.set("timestamp", datetime.now().strftime("%H%M%S.%f")[:-3])


def message_factory(
    sentence_type: str, field_names: list, example_str: str
) -> NMEA_Message:
    """create a message class"""

    vals = [str(f) for f in example_str.split(",")]
    fields = OrderedDict(zip(field_names, vals))

    return NMEA_Message(sentence_type, fields)


def ssn_message() -> NMEA_Message:
    """
    see https://www.septentrio.com/system/files/support/asterx4_firmware_v4.10.0_reference_guide.pdf  # noqa

    $PSSN,HRP,142657.80,061222,152.236,,-0.708,0.084,,0.181,21,2,2.400,E*23

    """

    field_names = [
        "sentence_type",
        "timestamp",
        "date",
        "heading",
        "roll",
        "pitch",
        "heading_stdev",
        "roll_stdev",
        "pitch_stdev",
        "sats_used",
        "rtk_mode",
        "magnetic_variation",
        "mag_var_direction",
    ]

    example_str = "HRP,142657.80,061222,152.236,,-0.708,0.084,,0.181,21,2,2.400,E"

    return message_factory("PSSN", field_names, example_str)


def gga_message() -> NMEA_Message:
    """$GPGGA,115739.00,4158.8441367,N,09147.4416929,W,4,13,0.9,255.747,M,-32.00,M,01,0000*6E"""  # noqa

    field_names = [
        "timestamp",
        "lat",
        "NS",
        "lon",
        "EW",
        "fix_type",  # named gps_qual in pynmea2
        "nr_sattelites",
        "horizontal_dilution",
        "elevation",
        "M1",
        "geoid_height",
        "M2",
        "gps_age",
        "station_id",
    ]
    example_str = "130000.00,0000.3934834,N,00604.9127445,E,4,20,0.7,23.1169,M,47.3944,M,3.2,0000"  # noqa

    return message_factory("GPGGA", field_names, example_str)

class Pose(NamedTuple):
    """Represents a pose in 2D space"""

    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0

    @property
    def xy(self) -> Tuple[float, float]:
        return (self.x, self.y)

    @classmethod
    def from_gps(cls, lat: float, lon: float, heading: float) -> "Pose":
        """create pose from gps coordinates"""
        x, y = latlon_to_enu((lat, lon))
        theta = heading_to_theta(heading)

        return cls(x, y, theta)

    def to_gps(self) -> Tuple[float, float, float]:
        """convert pose to gps coordinates"""
        lat, lon = enu_to_latlon((self.x, self.y))
        heading = theta_to_heading(self.theta)

        return lat, lon, heading

    def __str__(self) -> str:
        return f"x={self.x:.3f}, y={self.y:.3f}, theta={self.theta:.3f}"

class Mock_GPS:
    """dummy gps, generates gps messages from pose,
    generates invalid fix now and then.
    Runs a socket server simulating a gps device"""

    PORT = 28000
    UPDATE_FREQ = 5  # Hz

    def __init__(self, n_valid: int = 100, n_invalid: int = 0) -> None:
        """n_valid: number of valid fixes before invalid fix,
        n_invalid: number of invalid fixes before valid fix"""

        self._log = logging.getLogger("mock_gps")

        self._gga = gga_message()
        self._ssn = ssn_message()

        # fix quality list
        self._fix_qual = [4] * n_valid + [0] * n_invalid
        self._fix_counter = 0  # update on gga message

        self.pose = Pose()
        self._server: asyncio.Server | None = None

    def set_pose(self, x: float, y: float, theta: float) -> None:
        """set pose"""
        self.pose = Pose(x, y, theta)

    def nmea_gga(self) -> str:
        """generate gga message (position)"""

        lat, lon, _ = self.pose.to_gps()

        self._gga.timestamp_now()
        for k, v in zip(("lat", "NS", "lon", "EW"), sd_to_dm(lat, lon)):
            self._gga.set(k, v)

        # update fix quality
        self._gga.set("fix_type", str(self._fix_qual[self._fix_counter]))
        self._fix_counter = (self._fix_counter + 1) % len(self._fix_qual)

        return str(self._gga)

    def nmea_ssn(self) -> str:
        """generate ssn message (heading)"""
        heading = theta_to_heading(self.pose.theta)
        self._ssn.timestamp_now()
        self._ssn.set("heading", f"{heading:.3f}")

        return str(self._ssn)

    async def _send_data(self, writer: asyncio.StreamWriter) -> None:
        """Send GPS data to a connected client"""
        try:
            while True:
                # Send both GGA and SSN messages
                messages = [self.nmea_gga(), self.nmea_ssn()]
                for message in messages:
                    writer.write(f"{message}\r\n".encode())
                    self._log.debug(f"Sent: {message}")

                try:
                    await writer.drain()
                except ConnectionError as e:
                    self._log.warning(f"Conection error: {e}")
                    return

                await asyncio.sleep(1 / self.UPDATE_FREQ)  # Sleep according to update frequency
        except ConnectionError as e:
            self._log.warning(f"Conection error: {e}")
        except Exception as e:
            self._log.error(f"Error sending data: {e}")
        finally:
            try:
                writer.close()
                try:
                    await asyncio.wait_for(writer.wait_closed(), timeout=1.0)
                except asyncio.TimeoutError:
                    self._log.warning("Timeout waiting for connection to close")
            except ConnectionError as e:
                self._log.warning(f"Conection error: {e}")



    async def _handle_client(
        self,
        _: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ) -> None:
        """Handle a client connection"""
        addr = writer.get_extra_info('peername')
        self._log.info(f"Client connected from {addr}")
        await self._send_data(writer)

    async def _start_server(self) -> None:
        """Start the GPS server"""
        self._server = await asyncio.start_server(
            self._handle_client,
            host='0.0.0.0',  # Listen on all interfaces
            port=self.PORT,
            reuse_address=True
        )

        if self._server.sockets:
            addr = self._server.sockets[0].getsockname()
            self._log.info(f"Mock GPS server listening on {addr[0]}:{addr[1]}")

    async def _stop_server(self) -> None:
        """Stop the GPS server"""
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            self._log.info("GPS server stopped")

    async def main(self) -> None:
        """Start serving gps data over a socket connection"""


        try:
            await self._start_server()
            if self._server is None:
                raise RuntimeError("Server not started")
            await self._server.serve_forever()
        except asyncio.CancelledError:
            self._log.info("Cancelled")
        except Exception as e:
            self._log.error(f"Server error: {e}")
        finally:
            await self._stop_server()

class MockRobot:
    """simulate a robot that drives around in circles around origin"""

    RADIUS = 25.0  # meters
    SPEED = 1.0  # meters per second

    def __init__(self) -> None:
        self.x = self.RADIUS  # start on x-axis
        self.y = 0.0
        self.theta = 0.0  # start facing forward (along y-axis)

        self.gps = Mock_GPS()

    async def sim_loop(self, dt: float = 0.1) -> None:
        """simulate robot movement"""

        while True:
            # Update theta (negative for counterclockwise motion)
            self.theta += self.SPEED * dt / self.RADIUS

            # Calculate position - use correct parametric circle equations
            self.x = self.RADIUS * math.cos(self.theta)
            self.y = self.RADIUS * math.sin(self.theta)

            # print(f"{self.x:.1f}, {self.y:.1f}, theta: {self.theta:.3f} rad ({math.degrees(self.theta):.1f} deg)")

            # clip theta to 2pi
            self.theta %= 2 * math.pi

            self.gps.set_pose(self.x, self.y, self.theta + math.pi/2)

            await asyncio.sleep(dt)

    async def main(self) -> None:
        log.info("Starting mock robot")
        log.info(f"{GPS_REF=}")

        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.gps.main())
            tg.create_task(self.sim_loop())



def main() -> None:



    async def main() -> None:
        robot = MockRobot()
        await robot.main()

    run_main_async(main())


if __name__ == "__main__":
    main()

