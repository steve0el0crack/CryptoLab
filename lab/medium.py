from __future__ import annotations
from abc import abstractmethod, ABC
from typing import Any

from lab.misc import NetworkParticipantId, Coordinate, Area

class NetworkParticipant(ABC):
    def __init__(self, identity: NetworkParticipantId, position: Coordinate):
        self.identity = identity
        self.position = position

    def get_id(self) -> NetworkParticipantId:
        return self.identity

    def get_position(self) -> Coordinate:
        return self.position

    def initialize_world(self, world: Medium) -> None:
        pass

    @abstractmethod
    def get_coverage_area(self) -> Area:
        pass

    @abstractmethod
    def receive_message(self, world: Medium, source: NetworkParticipant, msg: Any) -> bool:
        return True

    def broadcast_message(self, world: Medium, msg: Any) -> None:
        world.broadcast_message(self, msg)

    def broadcast_message_directed(self, world: Medium, target: NetworkParticipant, msg: Any) -> None:
        world.directed_broadcast_message(self, msg, target)


class Medium:
    def __init__(self):
        self.participants = {}
        self.simulation_steps = []

    def register(self, entity: NetworkParticipant|list) -> None:
        if isinstance(entity, NetworkParticipant):
            self.participants[entity.get_id()] = entity
            entity.initialize_world(self)
        elif isinstance(entity, list):
            for item in entity:
                self.register(item)
        else:
            raise NotImplementedError

    def _simulated_msg_delivery(self, source: NetworkParticipant, message: Any, target: NetworkParticipant, on_medium_type: str, failed: bool = False) -> None:
        self.simulation_steps.append((source, message, target, on_medium_type, failed))

    def broadcast_message(self, source: NetworkParticipant, message: Any) -> None:
        src_coverage = source.get_coverage_area()
        if src_coverage is None:
            return
        for participant in self.participants:
            if src_coverage.is_in_range(self.participants[participant].get_position()):
                self._simulated_msg_delivery(source, message, self.participants[participant], "u-message")

    def directed_broadcast_message(self, source: NetworkParticipant, message: Any, target: NetworkParticipant|NetworkParticipantId) -> None:
        if isinstance(target, NetworkParticipantId):
            target = self.participants[target]
        src_coverage = source.get_coverage_area()
        if src_coverage is None:
            return
        if src_coverage.is_in_range(target.get_position()):
            self._simulated_msg_delivery(source, message, target, "d-message")
        else:
            self._simulated_msg_delivery(source, message, target, "d-message", True)
        # TODO also transmit to other participants?

    def send_message_wired(self, source: NetworkParticipant, message: Any, target: NetworkParticipant|NetworkParticipantId) -> None:
        if isinstance(target, NetworkParticipantId):
            target = self.participants[target]
        self._simulated_msg_delivery(source, message, target, "w-message")

    def wired_broadcast(self, source: NetworkParticipant, message: Any, id_type: str) -> None:
        for participant in self.participants:
            if participant.id_type == id_type:
                self._simulated_msg_delivery(source, message, self.participants[participant], "t-message")

    def simulate(self) -> None:
        queued_steps = self.simulation_steps.copy()
        self.simulation_steps.clear()
        for (source, message, target, on_medium_type, failed) in queued_steps:
            if source == target:
                continue
            if failed:
                print(
                    f"{target.get_id()}: Supposed to receive {on_medium_type} from {source.get_id()} > {message}, but out of range")
                continue
            if target.receive_message(self, source, message):
                print(f"{target.get_id()}: Received {on_medium_type} from {source.get_id()} > {message}")

    def is_done_simulating(self) -> bool:
        return len(self.simulation_steps) == 0