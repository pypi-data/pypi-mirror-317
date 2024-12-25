from datetime import datetime, timezone, timedelta

from ldkex.archive import Metadata
from ldkex.utils import read_coordinate, read_int, get_metadata_version, read_long


class Location:
    def __init__(self, file, version):
        self.size = read_int(file)
        current_location = file.tell()
        end_location = current_location + self.size
        self.longitude = read_coordinate(file)
        self.latitude = read_coordinate(file)
        self.date = None

        if version == 101:
            self._process_version_101(file, end_location)
        elif version == 2:
            self._process_version_2(file)

        file.seek(end_location)

    def _process_version_101(self, file, end_location):
        while file.tell() < end_location:
            data_type_byte = file.read(1)
            if not data_type_byte:
                break
            if data_type_byte == b'\x74':  # UTC time byte
                utc_time = self.resolve_utc_time(file)
                if self._set_date(utc_time):
                    break
            else:
                self.skip_data(file, data_type_byte)

    def _process_version_2(self, file):
        file.seek(4, 1)  # Skip 4 bytes
        utc_time = self.resolve_utc_time(file)
        self._set_date(utc_time)

    def _set_date(self, utc_time):
        if utc_time and utc_time.year >= 2000:
            kyiv_offset = timedelta(hours=3 if 3 <= utc_time.month <= 10 else 2)
            self.date = utc_time.astimezone(timezone(kyiv_offset)).strftime('%Y-%m-%dT%H:%M:%S')
            return True
        print(f"Invalid year: {utc_time.year}" if utc_time else "Invalid UTC time")
        return False

    @staticmethod
    def resolve_utc_time(file):
        timestamp = read_long(file)
        try:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        except Exception as e:
            print(f"Invalid timestamp: {timestamp}")
            return None

    @staticmethod
    def skip_data(file, data_type_byte):
        size_map = {
            b'\x61': 4, b'\x62': 1, b'\x65': 4, b'\x6e': 2,
            b'\x70': 4, b'\x73': 8, b'\x76': 4,
        }
        file.read(size_map.get(data_type_byte, 0))


class Locations:
    def __init__(self, file, version):
        self.locations_count = read_int(file)
        self.locations = []

        for i in range(self.locations_count):
            try:
                self.locations.append(Location(file, version))
            except Exception as e:
                print("Location content does not meet doc specification")
                break


class AreaPolygon:
    def __init__(self, file, version):
        self.metadata = Metadata(file, get_metadata_version(version, "are"))
        self.locations = Locations(file, version)
        self.number_of_holes = read_int(file)
        self.holes = []

        for _ in range(self.number_of_holes):
            try:
                self.holes.append(Locations(file, version))
            except Exception as e:
                print("Locations content does not meet doc specification")
                break


class AreaPolygons:
    def __init__(self, file, version):
        self.polygons_count = read_int(file)
        self.polygons = []

        for _ in range(self.polygons_count):
            try:
                self.polygons.append(AreaPolygon(file, version))
            except Exception as e:
                print("AreaPolygon content does not meet doc specification")
                break


class AreaFile:
    def __init__(self, file, file_metadata_map):
        self.file_metadata_map = file_metadata_map
        self.magic_number = read_int(file)
        file_magic = (self.magic_number >> 8) & 0xFFFFFF  # Shift right by 8 bits and mask with 0xFFFFFF
        version = self.magic_number & 0xFF  # Mask with 0xFF

        if (self.magic_number & 0x50500000) == 0x50500000:
            version = (self.magic_number & 0xFF) + 100

        if file_magic != 0x50500D:
            print(f"Area file magic: {file_magic} version: {version}")

        self.header_size = read_int(file)

        if version < 100:
            file.seek(file.tell() + self.header_size)
        else:
            _ = Metadata(file, get_metadata_version(version, "are"))

        self.metadata = Metadata(file, get_metadata_version(version, "are"))
        self.polygons = AreaPolygons(file, version)


class Waypoint:
    def __init__(self, file, version, file_type):
        self.metadata = Metadata(file, get_metadata_version(version, file_type))
        self.location = Location(file, version)


class Waypoints:
    def __init__(self, file, version, file_type):
        self.waypoints_count = read_int(file)
        self.waypoints = []

        for _ in range(self.waypoints_count):
            try:
                self.waypoints.append(Waypoint(file, version, file_type))
            except Exception as e:
                print("Waypoint content does not meet doc specification")
                break


class RouteFile:
    def __init__(self, file, file_metadata_map):
        self.file_metadata_map = file_metadata_map
        self.magic_number = read_int(file)
        file_magic = (self.magic_number >> 8) & 0xFFFFFF  # Shift right by 8 bits and mask with 0xFFFFFF
        version = self.magic_number & 0xFF  # Mask with 0xFF

        if (self.magic_number & 0x50500000) == 0x50500000:
            version = (self.magic_number & 0xFF) + 100

        if file_magic != 0x50500C:
            print(f"Route file magic: {file_magic} version: {version}")

        self.header_size = read_int(file)

        if version < 100:
            file.seek(file.tell() + self.header_size)
        else:
            _ = Metadata(file, get_metadata_version(version, "rte"))

        self.metadata = Metadata(file, get_metadata_version(version, "rte"))
        self.waypoints = Waypoints(file, version, "rte")


class TrackSegment:
    def __init__(self, file, version, file_type):
        if version >= 3:
            self.metadata = Metadata(file, get_metadata_version(version, "trk"))
        else:
            read_int(file)
        self.locations = Locations(file, version)


class TrackSegments:
    def __init__(self, file, version, file_type):
        try:
            self.segments_count = read_int(file)
        except Exception as e:
            print("TrackSegments content does not meet doc specification")
            self.segments_count = 0
        self.segments = []

        for _ in range(self.segments_count):
            try:
                self.segments.append(TrackSegment(file, version, file_type))
            except Exception as e:
                print("TrackSegment content does not meet doc specification")
                break


class TrackFile:
    def __init__(self, file, file_metadata_map):
        self.file_metadata_map = file_metadata_map
        self.magic_number = read_int(file)
        file_magic = (self.magic_number >> 8) & 0xFFFFFF  # Shift right by 8 bits and mask with 0xFFFFFF
        version = self.magic_number & 0xFF  # Mask with 0xFF

        if (self.magic_number & 0x50500000) == 0x50500000:
            version = (self.magic_number & 0xFF) + 100

        if file_magic != 0x50500E:
            print(f"Track file magic: {file_magic} version: {version}")

        self.header_size = read_int(file)

        if version < 100:
            file.seek(file.tell() + self.header_size)
        else:
            _ = Metadata(file, get_metadata_version(version, "trk"))

        self.metadata = Metadata(file, get_metadata_version(version, "trk"))
        self.waypoints = Waypoints(file, version, "trk")
        self.track_segments = TrackSegments(file, version, "set")


class WaypointFile:
    def __init__(self, file, file_metadata_map):
        self.file_metadata_map = file_metadata_map
        self.magic_number = read_int(file)
        file_magic = (self.magic_number >> 8) & 0xFFFFFF  # Shift right by 8 bits and mask with 0xFFFFFF
        version = self.magic_number & 0xFF  # Mask with 0xFF

        if (self.magic_number & 0x50500000) == 0x50500000:
            version = (self.magic_number & 0xFF) + 100

        if file_magic != 0x50500A:
            print(f"Wpt file magic: {file_magic} version: {version}")

        self.header_size = read_int(file)
        file.seek(file.tell() + self.header_size)
        self.waypoint = Waypoint(file, version, "wpt")


class PointsSet:
    def __init__(self, file):
        self.magicNumber = read_int(file)
        fileMagic = (self.magicNumber >> 8) & 0xFFFFFF
        version = self.magicNumber & 0xFF
        if (self.magicNumber & 0x50500000) == 0x50500000:
            version = (self.magicNumber & 0xFF) + 100

        if fileMagic != 0x50500B:
            print(f"Set file magic: {fileMagic} version: {version}")

        self.headerSize = read_int(file)

        if version < 100:
            file.seek(file.tell() + self.headerSize)
        else:
            Metadata(file, get_metadata_version(version, "set"))

        self.metadata = Metadata(file, get_metadata_version(version, "set"))
        self.waypoints = Waypoints(file, version, "set")


class PointsSetFile:
    def __init__(self, file, file_metadata_map):
        self.file_metadata_map = file_metadata_map
        self.magicNumber = read_int(file)
        fileMagic = (self.magicNumber >> 8) & 0xFFFFFF
        version = self.magicNumber & 0xFF
        if (self.magicNumber & 0x50500000) == 0x50500000:
            version = (self.magicNumber & 0xFF) + 100

        if fileMagic != 0x50500B:
            print(f"Set file magic: {fileMagic} version: {version}")

        self.headerSize = read_int(file)

        if version < 100:
            file.seek(file.tell() + self.headerSize)
        else:
            Metadata(file, get_metadata_version(version, "set"))

        self.metadata = Metadata(file, get_metadata_version(version, "set"))
        self.waypoints = Waypoints(file, version, "set")
