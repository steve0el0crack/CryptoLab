from __future__ import annotations
import typing
from typing import Any

from medium import Medium, NetworkParticipant
from misc import NetworkParticipantId, Coordinate, CircularArea, RectangularArea, Area, RoadSegment, \
    RoadNetworkSubset
from protocol_types import ReportRoutes, AggregateRoutes, TrafficGuidance, RequestRoutes


class RSU(NetworkParticipant):
    def __init__(self, identity: NetworkParticipantId, position: Coordinate, responsible_tmc: NetworkParticipantId):
        super().__init__(identity, position)
        self.coverage = CircularArea(position, 1000)
        self.controlled_area = RectangularArea(position - Coordinate((1000, 1000)), position + Coordinate((1000, 1000)))
        self.aggregated = []
        self.report_threshold = 5
        self.responsible_tmc = responsible_tmc
        self.road_network = None

    def initialize_world(self, world: Medium) -> None:
        self.road_network = world.participants[self.responsible_tmc].road_network.create_subset_within_area(self.controlled_area)

    def get_coverage_area(self) -> Area:
        return self.coverage

    def receive_message(self, world: Medium, source: NetworkParticipant, msg: Any) -> bool:
        if isinstance(msg, ReportRoutes):
            self.protocol_report_routes(world, typing.cast(Vehicle, source), msg)
            return True
        if isinstance(msg, TrafficGuidance) and not isinstance(source, RSU):
            self.protocol_traffic_guidance(world, typing.cast(TMC, source), msg)
            return True
        return False

    def protocol_report_routes(self, world: Medium, _vehicle: Vehicle, msg: ReportRoutes) -> None:
        self.aggregated.append(msg.route)
        if len(self.aggregated) >= self.report_threshold:
            world.send_message_wired(self, AggregateRoutes(self.aggregated.copy()), self.responsible_tmc)
            self.aggregated.clear()

    def protocol_traffic_guidance(self, world: Medium, _tmc: TMC, msg: TrafficGuidance) -> None:
        self.broadcast_message(world, msg)

    def broadcast_request_routes(self, world: Medium) -> None:
        self.broadcast_message(world, RequestRoutes(self.road_network))


class Vehicle(NetworkParticipant):
    def __init__(self, identity: NetworkParticipantId, position: Coordinate, route: list[RoadSegment]):
        super().__init__(identity, position)
        self.coverage = CircularArea(position, 2500)
        self.route = route

    def get_coverage_area(self) -> Area:
        return self.coverage

    def receive_message(self, world: Medium, source: NetworkParticipant, msg: Any) -> bool:
        if isinstance(msg, RequestRoutes):
            self.protocol_request_routes(world, typing.cast(RSU, source), msg)
            return True
        if isinstance(msg, TrafficGuidance):
            self.protocol_traffic_guidance(world, typing.cast(RSU, source), msg)
            return True
        return False

    def protocol_request_routes(self, world: Medium, rsu: RSU, msg: RequestRoutes) -> None:
        report_vector = msg.road_network_subset.create_report_vector(self.route)
        self.broadcast_message_directed(world, rsu, ReportRoutes(report_vector))

    def protocol_traffic_guidance(self, world: Medium, _rsu: RSU, msg: TrafficGuidance) -> None:
        print(f"Applying traffic guidance {msg.msg} for vehicle {self.get_id()}")

class TMC(NetworkParticipant):

    def __init__(self, identity: NetworkParticipantId, position: Coordinate, area: Area, road_network: RoadNetworkSubset):
        super().__init__(identity, position)
        self.area = area
        self.road_network = road_network
        self.aggregated_routes = []

    def get_coverage_area(self) -> None:
        return None

    def receive_message(self, world: Medium, source: NetworkParticipant, msg: Any) -> bool:
        if isinstance(msg, AggregateRoutes):
            self.protocol_aggregate_routes(world, typing.cast(RSU, source), msg)
            return True
        return False

    def protocol_aggregate_routes(self, world: Medium, _rsu: RSU, msg: AggregateRoutes) -> None:
        self.aggregated_routes.append(msg.routes)
        world.wired_broadcast(self, TrafficGuidance(str(sum([sum([len(route) for route in agg_route]) for agg_route in self.aggregated_routes]))), "rsu")
