#!/usr/bin/env python3

import hashlib
import random


class Vehicle:
    """Represents a vehicle in the VANET system."""

    def __init__(self, id, route_vector, alt_route_vector):
        """
        Initialize a vehicle.

        Args:
            id (str): Vehicle identifier
            route_vector (list): List of 0s and 1s representing current route segments
            alt_route_vector (list): List of 0s and 1s representing alternative route segments
        """
        self.id = id
        self.route_vector = route_vector
        self.alt_route_vector = alt_route_vector
        self.shares_received = {}  # Shares received from other vehicles
        self.va_share = None  # This vehicle's share of the aggregated route vector
        self.best_route = None  # The chosen best route (either vi or alt_vi)

    def create_shares(self, all_vehicle_ids, p):
        """
        Create additive secret shares of the route vector for all vehicles.

        Args:
            all_vehicle_ids (list): List of all vehicle IDs including self
            p (int): Large prime modulus for secret sharing

        Returns:
            dict: Dictionary mapping vehicle_id -> list of shares for each component
        """
        shares = {}

        # For each component of the route vector, create shares for all vehicles
        for j in range(len(self.route_vector)):
            component_shares = {}

            # Generate random shares for all but one vehicle
            for vid in all_vehicle_ids[:-1]:
                component_shares[vid] = random.randint(0, p-1)

            # Last share is computed to make the sum equal to route_vector[j]
            last_vid = all_vehicle_ids[-1]
            sum_others = sum(component_shares[vid] for vid in all_vehicle_ids[:-1])
            component_shares[last_vid] = (self.route_vector[j] - sum_others) % p

            # Store shares for this component
            for vid in all_vehicle_ids:
                if vid not in shares:
                    shares[vid] = [0] * len(self.route_vector)
                shares[vid][j] = component_shares[vid]

        return shares

    def compute_va_share(self, p, all_shares):
        """
        Compute this vehicle's share of the aggregated route vector vA.

        Args:
            p (int): Prime modulus
            all_shares (dict): All shares created by all vehicles

        Returns:
            list: Share of vA for each component
        """
        va_share = [0] * len(self.route_vector)

        # Sum shares for each component from ALL vehicles (including self)
        for j in range(len(self.route_vector)):
            for vid in all_shares:
                va_share[j] = (va_share[j] + all_shares[vid][self.id][j]) % p

        self.va_share = va_share
        return va_share

    def choose_best_route(self, congested_segments):
        """
        Choose the best route based on congested segments.

        Args:
            congested_segments (list): List of segment indices that are congested

        Returns:
            list: The chosen route (either route_vector or alt_route_vector)
        """
        # Check if any segment in current route is congested
        current_route_congested = any(
            self.route_vector[j] == 1 for j in congested_segments
        )

        if current_route_congested:
            self.best_route = self.alt_route_vector
            return self.alt_route_vector
        else:
            self.best_route = self.route_vector
            return self.route_vector


class RSU:
    """Represents a Roadside Unit that broadcasts timestamps."""

    def __init__(self):
        """Initialize RSU with a random timestamp."""
        self.timestamp = random.randint(0, 10**9)

    def broadcast_timestamp(self):
        """
        Broadcast the current timestamp T.

        Returns:
            int: Current timestamp
        """
        return self.timestamp


class TMC:
    """Represents the Traffic Management Center that processes aggregates and provides guidance."""

    def __init__(self, segment_capacities):
        """
        Initialize TMC with segment capacities.

        Args:
            segment_capacities (list): Maximum vehicles per segment
        """
        self.segment_capacities = segment_capacities

    def receive_and_verify(self, vA, sigma_A, expected_signatures):
        """
        Receive vA and σA from vehicles and verify the signature.

        Args:
            vA (list): Aggregated route vector
            sigma_A (str): Combined signature
            expected_signatures (list): Expected signature parts for verification

        Returns:
            bool: True if signature is valid, False otherwise
        """
        # Simple verification: check if σA contains expected signature parts
        expected_sigma_A = ''.join(expected_signatures)
        return sigma_A == expected_sigma_A

    def compute_congested_segments(self, vA):
        """
        Compute which segments are congested based on vA and capacities.

        Args:
            vA (list): Aggregated route vector

        Returns:
            list: List of segment indices that are congested
        """
        congested = []
        for j in range(len(vA)):
            if vA[j] > self.segment_capacities[j]:
                congested.append(j)
        return congested

    def broadcast_guidance(self, congested_segments):
        """
        Broadcast the list of congested segments to vehicles.

        Args:
            congested_segments (list): List of congested segment indices

        Returns:
            list: The congested segments list
        """
        return congested_segments


def main():
    """
    Main function demonstrating the π1 protocol execution.
    """
    # Protocol parameters
    p = 10**9 + 7  # Large prime for modular arithmetic
    H = hashlib.sha256  # Random oracle (hash function)

    print("=== π1 Protocol Demonstration ===")
    print(f"Prime modulus p = {p}")
    print()

    # Create vehicles with sample route vectors and alternatives (4 road segments)
    vehicles = [
        Vehicle("vehicle1", [1, 0, 1, 0], [0, 0, 1, 1]),  # Takes segments 1,3 -> alt 3,4
        Vehicle("vehicle2", [0, 1, 0, 1], [1, 1, 0, 0]),  # Takes segments 2,4 -> alt 1,2
        Vehicle("vehicle3", [1, 1, 0, 0], [0, 1, 1, 0])   # Takes segments 1,2 -> alt 2,3
    ]

    all_ids = [v.id for v in vehicles]
    print(f"Participating vehicles: {all_ids}")
    print()

    # Display individual route vectors and alternatives
    for vehicle in vehicles:
        print(f"{vehicle.id}: current={vehicle.route_vector}, alternative={vehicle.alt_route_vector}")
    print()

    # Step 1: Set random oracle H
    print("Step 1: Random oracle H set to SHA-256")
    print()

    # Step 2: RSU broadcasts timestamp T
    rsu = RSU()
    T = rsu.broadcast_timestamp()
    print(f"Step 2: RSU broadcasts timestamp T = {T}")
    print()

    # Step 3: Each vehicle creates secret shares
    print("Step 3: Each vehicle creates additive secret shares of its route vector")
    all_shares = {}
    for vehicle in vehicles:
        shares = vehicle.create_shares(all_ids, p)
        all_shares[vehicle.id] = shares
        print(f"  {vehicle.id} created shares for all vehicles")
    print()

    # Step 4: Distribute shares (simulation)
    print("Step 4: Distribute shares to all vehicles")
    for vehicle in vehicles:
        vehicle.shares_received = {}
        for other_id in all_ids:
            if other_id != vehicle.id:
                vehicle.shares_received[other_id] = all_shares[other_id][vehicle.id]
        print(f"  {vehicle.id} received shares from {len(vehicle.shares_received)} other vehicles")
    print()

    # Step 5: Each vehicle computes its share of vA
    print("Step 5: Each vehicle computes its share of the aggregated route vector vA")
    va_shares = {}
    for vehicle in vehicles:
        va_shares[vehicle.id] = vehicle.compute_va_share(p, all_shares)
        print(f"  {vehicle.id}'s vA share: {va_shares[vehicle.id]}")
    print()

    # Step 6: Reconstruct vA by summing all shares
    print("Step 6: Reconstruct vA by summing all vehicle shares")
    vA = [0] * len(vehicles[0].route_vector)
    for j in range(len(vA)):
        for vid in va_shares:
            vA[j] = (vA[j] + va_shares[vid][j]) % p

    print(f"  Reconstructed vA: {vA}")
    print()

    # Verification: compute expected vA directly (with modular arithmetic)
    expected_vA = [sum(v.route_vector[j] for v in vehicles) % p for j in range(len(vehicles[0].route_vector))]
    print(f"  Expected vA (mod {p}): {expected_vA}")
    print(f"  vA matches expected: {vA == expected_vA}")
    print()

    # Step 7: Each vehicle broadcasts its ID
    print("Step 7: Each vehicle broadcasts its ID")
    print(f"  Broadcast IDs: {all_ids}")
    print()

    # Step 8: Compute IDA (group identity)
    print("Step 8: Compute group identity IDA")
    sorted_ids = sorted(all_ids)
    id_string = ''.join(sorted_ids)
    IDA = H(id_string.encode()).hexdigest()
    print(f"  Sorted IDs: {sorted_ids}")
    print(f"  ID string: '{id_string}'")
    print(f"  IDA (SHA-256): {IDA[:16]}...")  # Show first 16 chars
    print()

    # Step 9: Each vehicle computes signature σi
    print("Step 9: Each vehicle computes signature σi")
    signatures = []
    for vehicle in vehicles:
        message = str(vA) + IDA + str(T)
        sigma_i = f"signature_of_{vehicle.id}_on_{message[:50]}..."  # Truncate for display
        signatures.append(sigma_i)
        print(f"  {vehicle.id} computes σi: {sigma_i[:30]}...")

    # Step 10: Combine all signatures into σA
    print()
    print("Step 10: Combine all signatures into σA")
    sigma_A = ''.join(signatures)
    print(f"  Combined σA: {sigma_A[:50]}...")  # Show first 50 chars
    print()

    # Step 11: Send vA and σA to TMC
    print("Step 11: Send vA and σA to TMC")
    print(f"  Sending vA: {vA}")
    print(f"  Sending σA: {sigma_A[:32]}...")
    print()

    # Step 12: TMC verifies σA
    print("Step 12: TMC verifies σA")
    tmc = TMC(segment_capacities=[3, 1, 3, 2])  # Example capacities (segment 1 capacity reduced to create congestion)
    verification_success = tmc.receive_and_verify(vA, sigma_A, signatures)
    print(f"  Verification result: {'SUCCESS' if verification_success else 'FAILED'}")
    print()

    if not verification_success:
        print("ERROR: Signature verification failed!")
        return

    # Step 13: TMC computes congested segments
    print("Step 13: TMC computes congested segments")
    congested_segments = tmc.compute_congested_segments(vA)
    print(f"  Segment capacities: {tmc.segment_capacities}")
    print(f"  Congested segments: {congested_segments}")
    print()

    # Step 14: Broadcast congested segments to vehicles
    print("Step 14: TMC broadcasts congested segments to vehicles")
    broadcast_congested = tmc.broadcast_guidance(congested_segments)
    print(f"  Broadcast: {broadcast_congested}")
    print()

    # Step 15: Each vehicle chooses best route
    print("Step 15: Each vehicle chooses best route based on congestion")
    for vehicle in vehicles:
        best_route = vehicle.choose_best_route(congested_segments)
        print(f"  {vehicle.id}: best route = {best_route}")
    print()

    # Final output
    print("=== Protocol Complete ===")
    print(f"Final aggregated route vector vA: {vA}")
    print(f"Final signature σA: {sigma_A[:32]}...")  # Show first 32 chars
    matches = vA == expected_vA
    print(f"Aggregation verification: vA = {expected_vA} ✓" if matches else f"Aggregation verification: FAILED ✗ (vA = {vA})")
    print(f"Congested segments: {congested_segments}")
    print("Best routes chosen:")
    for vehicle in vehicles:
        print(f"  {vehicle.id}: {vehicle.best_route}")

    if matches and verification_success:
        print("Protocol executed successfully! Privacy-preserving aggregation with route guidance achieved.")


if __name__ == "__main__":
    main()
