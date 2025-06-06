from entity import TMC, RSU, Vehicle
from medium import Medium
from misc import RoadNetworkSubset, RectangularArea, Coordinate, NetworkParticipantId

if __name__ == "__main__":
    simulation_world_medium = Medium()

    tmc_area = RectangularArea(Coordinate((-10000, -10000)), Coordinate((10000, 10000)))
    road_network = RoadNetworkSubset.random_road_network(10000, tmc_area)
    tmc = TMC(NetworkParticipantId.random_id("tmc", 0), Coordinate((0, 0)), tmc_area, road_network)
    rsu_list = [RSU(NetworkParticipantId.random_id("rsu", index), tmc_area.random_point(), tmc.get_id()) for index in range(10)]
    vehicle_list = [Vehicle(NetworkParticipantId.random_id("v", index), tmc_area.random_point(), road_network.random_route()) for index in range(100)]

    simulation_world_medium.register(tmc)
    simulation_world_medium.register(rsu_list)
    simulation_world_medium.register(vehicle_list)

    # Main Simulation

    simulation_steps = 0
    max_steps = 15
    while not simulation_world_medium.is_done_simulating() or simulation_steps == 0 or simulation_steps > max_steps:
        print(f"----- Step {simulation_steps} -----")
        if simulation_steps < 5:
            for rsu in rsu_list:
                rsu.broadcast_request_routes(simulation_world_medium)
        simulation_world_medium.simulate()
        simulation_steps += 1


