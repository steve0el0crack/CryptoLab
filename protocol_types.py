import dataclasses

from misc import RoadNetworkSubset


@dataclasses.dataclass
class RequestRoutes: # RSU -> Vehicle
    road_network_subset: RoadNetworkSubset

@dataclasses.dataclass
class ReportRoutes:
    route: list[int]

@dataclasses.dataclass
class AggregateRoutes:
    routes: list[list[int]]

@dataclasses.dataclass
class TrafficGuidance:
    msg: str