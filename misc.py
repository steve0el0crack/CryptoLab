from __future__ import annotations

import dataclasses
import math
import random
import uuid

@dataclasses.dataclass(frozen=True)
class Coordinate:
    _tuple: (int, int)

    def get_coordinates(self) -> (int, int):
        return self._tuple

    def distance(self, other: Coordinate) -> float:
        return math.pow((self._tuple[0] - other._tuple[0]) ** 2 + (self._tuple[1] - other._tuple[1]) ** 2, 1/2)

    def __add__(self, other) -> Coordinate:
        if isinstance(other, Coordinate):
            return Coordinate((self._tuple[0] + other._tuple[0], self._tuple[1] + other._tuple[1]))
        raise NotImplementedError

    def __sub__(self, other) -> Coordinate:
        if isinstance(other, Coordinate):
            return Coordinate((self._tuple[0] - other._tuple[0], self._tuple[1] - other._tuple[1]))
        raise NotImplementedError

    def __mul__(self, other) -> Coordinate:
        if isinstance(other, int) or isinstance(other, float):
            return Coordinate((self._tuple[0] * other, self._tuple[1] * other))
        raise NotImplementedError

    def __truediv__(self, other) -> Coordinate:
        if isinstance(other, int) or isinstance(other, float):
            return Coordinate((self._tuple[0] / other, self._tuple[1] / other))
        raise NotImplementedError

@dataclasses.dataclass(frozen=True)
class RoadSegment:
    begin: Coordinate
    end: Coordinate

class Area:
    def __init__(self):
        pass

    def is_in_range(self, coordinate: Coordinate) -> bool:
        return False

@dataclasses.dataclass(frozen=True)
class CircularArea(Area):
    _center: Coordinate
    _radius: float

    def is_in_range(self, coordinate: Coordinate) -> bool:
        return self._center.distance(coordinate) <= self._radius

@dataclasses.dataclass(frozen=True, init=False)
class RectangularArea(Area):
    _min: Coordinate
    _max: Coordinate

    def __init__(self, vertex1: Coordinate, vertex2: Coordinate):
        super().__init__()
        object.__setattr__(self, "_min", Coordinate((min(vertex1.get_coordinates()[0], vertex2.get_coordinates()[0]),
                                                     min(vertex1.get_coordinates()[1], vertex2.get_coordinates()[1]))))
        object.__setattr__(self, "_max", Coordinate((max(vertex1.get_coordinates()[0], vertex2.get_coordinates()[0]),
                                                     max(vertex1.get_coordinates()[1], vertex2.get_coordinates()[1]))))

    def is_in_range(self, coordinate: Coordinate) -> bool:
        return self._min.get_coordinates()[0] < coordinate.get_coordinates()[0] < self._max.get_coordinates()[0] \
            and self._min.get_coordinates()[1] < coordinate.get_coordinates()[1] < self._max.get_coordinates()[1]

    def random_point(self) -> Coordinate:
        return Coordinate((random.randint(self._min.get_coordinates()[0], self._max.get_coordinates()[0]), random.randint(self._min.get_coordinates()[1], self._max.get_coordinates()[1])))

@dataclasses.dataclass(frozen=True, init=False)
class RoadNetworkSubset:
    id_to_segments: list[RoadSegment]
    segments_to_id: dict[RoadSegment, int]

    def __init__(self, segments: list[RoadSegment]):
        object.__setattr__(self, "id_to_segments", segments)
        object.__setattr__(self, "segments_to_id", {self.id_to_segments[index]: index for index in range(len(self.id_to_segments))})

    def get_road_segment(self, index: int) -> RoadSegment | None:
        return self.id_to_segments[index] if index in range(len(self.id_to_segments)) else None

    def get_segment_id(self, road_segment: RoadSegment) -> int | None:
        return self.segments_to_id[road_segment] if road_segment in self.segments_to_id else None

    def create_subset_within_area(self, area: Area) -> RoadNetworkSubset:
        return RoadNetworkSubset([segment for segment in self.id_to_segments if area.is_in_range(segment.end) or area.is_in_range(segment.end)]) # This does not look right

    @staticmethod
    def random_road_network(n: int, area: RectangularArea) -> RoadNetworkSubset:
        return RoadNetworkSubset([RoadSegment(area.random_point(), area.random_point()) for _index in range(n)])

    def create_report_vector(self, route: list[RoadSegment]) -> list[int]:
        encoded_segments = [self.get_segment_id(segment) for segment in route]
        # encoded_segments.remove(None)
        return encoded_segments

    def random_route(self, min_len: int = 3, max_len: int = 8) -> list[RoadSegment]:
        return random.sample(self.id_to_segments, random.randint(min_len, max_len))

@dataclasses.dataclass(frozen=True, repr=False)
class NetworkParticipantId:
    id: uuid
    id_type: str
    id_index: int

    @staticmethod
    def random_id(id_type: str, id_index: int) -> NetworkParticipantId:
        return NetworkParticipantId(uuid.uuid4(), id_type, id_index)

    def __repr__(self):
        return f"{self.id_type}-{self.id_index} ({self.id})"