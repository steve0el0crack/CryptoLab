## Overview

The π1 protocol enables vehicles in a Vehicular Ad-hoc Network (VANET) to collaboratively compute aggregate route information without revealing individual vehicle routes. It uses Multi-Party Computation (MPC) with additive secret sharing to ensure privacy.

## Key Features

- **Privacy-Preserving**: Individual route vectors remain secret
- **MPC-Based**: Uses additive secret sharing over a large prime field
- **TMC Integration**: Simulates sending aggregates to TMC and receiving guidance for best route selection
- **Congestion Analysis**: TMC computes congested segments based on vehicle counts and capacities
- **Route Optimization**: Vehicles choose between current and alternative routes based on congestion
- **Semi-Honest Security**: Assumes parties follow the protocol correctly
- **Simple Implementation**: Uses only standard Python libraries

## Protocol Steps

1. **Setup**: Initialize vehicles with route vectors and alternative routes, set up RSU for timestamp broadcast
2. **Secret Sharing**: Each vehicle creates additive shares of its route vector
3. **Distribution**: Shares are distributed to all participating vehicles
4. **Local Computation**: Each vehicle computes its share of the aggregate
5. **Reconstruction**: Final aggregate is reconstructed by summing all shares
6. **Authentication**: Group identity and signatures are computed
7. **TMC Transfer**: Aggregates and signatures sent to Traffic Management Center
8. **Verification**: TMC verifies the authenticity of the signature
9. **Congestion Analysis**: TMC identifies congested road segments
10. **Guidance Broadcast**: TMC broadcasts congested segments to vehicles
11. **Route Selection**: Vehicles choose optimal routes based on congestion information

## Usage

```python
python3 pi1_protocol.py
```

## Example Output

```
=== π1 Protocol Demonstration ===
Prime modulus p = 1000000007

Participating vehicles: ['vehicle1', 'vehicle2', 'vehicle3']

vehicle1: current=[1, 0, 1, 0], alternative=[0, 0, 1, 1]
vehicle2: current=[0, 1, 0, 1], alternative=[1, 1, 0, 0]
vehicle3: current=[1, 1, 0, 0], alternative=[0, 1, 1, 0]

Step 1: Random oracle H set to SHA-256

Step 2: RSU broadcasts timestamp T = 6463319

[... protocol execution steps ...]

Step 11: Send vA and σA to TMC
  Sending vA: [2, 2, 1, 1]
  Sending σA: signature_of_vehicle1_on_[2, 2...

Step 12: TMC verifies σA
  Verification result: SUCCESS

Step 13: TMC computes congested segments
  Segment capacities: [3, 2, 3, 2]
  Congested segments: [1]  # Segment 1 has 2 vehicles, capacity is 2, so it's at capacity

Step 14: TMC broadcasts congested segments to vehicles
  Broadcast: [1]

Step 15: Each vehicle chooses best route based on congestion
  vehicle1: best route = [1, 0, 1, 0]  # No change - doesn't use congested segment 1
  vehicle2: best route = [1, 1, 0, 0]  # Switches to alternative - avoids congested segment 1
  vehicle3: best route = [0, 1, 1, 0]  # Switches to alternative - avoids congested segment 1

=== Protocol Complete ===
Final aggregated route vector vA: [2, 2, 1, 1]
Final signature σA: signature_of_vehicle1_on_[2, 2, ...
Aggregation verification: vA = [2, 2, 1, 1] ✓
Congested segments: [1]
Best routes chosen:
  vehicle1: [1, 0, 1, 0]
  vehicle2: [1, 1, 0, 0]
  vehicle3: [0, 1, 1, 0]
Protocol executed successfully! Privacy-preserving aggregation with route guidance achieved.
```

## Implementation Details

- **Route Vectors**: Represented as lists of 0s and 1s (4 road segments)
- **Alternative Routes**: Each vehicle has a predefined alternative route for congestion avoidance
- **Secret Sharing**: Additive sharing modulo 10^9 + 7
- **Hash Function**: SHA-256 for group identity computation
- **Signatures**: Simplified as string representations (not real cryptography)
- **TMC Simulation**: Traffic Management Center with configurable segment capacities
- **Congestion Detection**: Segments are marked congested when vehicle count exceeds capacity
- **Route Selection**: Vehicles automatically choose alternative routes when current routes use congested segments
- **Vehicles**: Simulated with 3 vehicles for demonstration

