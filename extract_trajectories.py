#!/usr/bin/env python3
"""
Extract vehicle trajectories and events from CARLA data.
Useful for understanding what happened in the simulation.
"""

import csv
from collections import defaultdict

def extract_data(filepath='Carla_Validation_.DATA'):
    """Extract and organize the simulation data."""

    print("Reading CARLA data...")
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    print(f"Total records: {len(rows)}")

    # Extract key information
    timestamps = []
    positions_x = []  # Column 5-10 appear to be position data
    positions_y = []
    heading = []
    events = []

    for row in rows:
        try:
            timestamp = float(row[2])
            timestamps.append(timestamp)

            # Extract what appears to be position/sensor data
            heading.append(float(row[3]))  # Heading data ~12 degrees

            # These columns show movement patterns
            positions_x.append(float(row[5]))
            positions_y.append(float(row[6]))

            # Event detection (columns that are mostly zero)
            event_col_16 = float(row[16]) if len(row) > 16 else 0.0
            event_col_17 = float(row[17]) if len(row) > 17 else 0.0

            if event_col_16 > 0 or event_col_17 > 0:
                events.append({
                    'timestamp': timestamp,
                    'col_16': event_col_16,
                    'col_17': event_col_17,
                })
        except (ValueError, IndexError) as e:
            continue

    # Save trajectory data
    with open('trajectories.csv', 'w') as f:
        f.write('timestamp,heading,position_x,position_y\n')
        for i in range(len(timestamps)):
            f.write(f'{timestamps[i]:.2f},{heading[i]:.2f},{positions_x[i]:.2f},{positions_y[i]:.2f}\n')

    print(f"✓ Saved trajectory data to: trajectories.csv ({len(timestamps)} points)")

    # Save events
    if events:
        with open('events.csv', 'w') as f:
            f.write('timestamp,event_type_1,event_type_2\n')
            for event in events:
                f.write(f"{event['timestamp']:.2f},{event['col_16']:.2f},{event['col_17']:.2f}\n")

        print(f"✓ Saved event data to: events.csv ({len(events)} events)")

    # Statistics
    print(f"\nData Summary:")
    print(f"  Time range: {min(timestamps):.2f}s to {max(timestamps):.2f}s")
    print(f"  Position X range: {min(positions_x):.0f} to {max(positions_x):.0f}")
    print(f"  Position Y range: {min(positions_y):.0f} to {max(positions_y):.0f}")
    print(f"  Average heading: {sum(heading)/len(heading):.2f} degrees")
    print(f"  Events detected: {len(events)}")

    # Movement analysis
    total_distance = 0
    for i in range(1, len(positions_x)):
        dx = positions_x[i] - positions_x[i-1]
        dy = positions_y[i] - positions_y[i-1]
        distance = (dx*dx + dy*dy)**0.5
        total_distance += distance

    print(f"  Approximate total distance traveled: {total_distance:.0f} units")

    return timestamps, positions_x, positions_y, events

if __name__ == '__main__':
    extract_data()
    print("\n✓ Data extraction complete!")
    print("\nGenerated files:")
    print("  • trajectories.csv - Vehicle movement over time")
    print("  • events.csv - Detected events/collisions")
