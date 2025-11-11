#!/usr/bin/env python3
"""
Analyze CARLA simulation data to extract key information about the lost simulation.
This script uses only standard library - no external dependencies required.
"""

import csv
from collections import defaultdict

def load_and_analyze_data(filepath='Carla_Validation_.DATA'):
    """Load and analyze the CARLA simulation data."""
    print("=" * 70)
    print("CARLA SIMULATION DATA ANALYSIS")
    print("=" * 70)

    rows = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    print(f"\n📊 BASIC INFORMATION:")
    print(f"  Trial ID: {rows[0][0]}")
    print(f"  Configuration: {rows[0][1]}")
    print(f"  Total records: {len(rows):,}")
    print(f"  Columns per record: {len(rows[0])}")

    # Extract timestamps
    timestamps = [float(row[2]) for row in rows]
    print(f"\n⏱️  TIME ANALYSIS:")
    print(f"  Start time: {min(timestamps):.2f}s")
    print(f"  End time: {max(timestamps):.2f}s")
    print(f"  Duration: {max(timestamps) - min(timestamps):.2f}s")

    # Calculate timesteps
    time_diffs = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
    avg_timestep = sum(time_diffs) / len(time_diffs)
    print(f"  Average timestep: {avg_timestep:.4f}s")
    print(f"  Sampling rate: ~{1/avg_timestep:.1f} Hz")
    print(f"  Min timestep: {min(time_diffs):.4f}s")
    print(f"  Max timestep: {max(time_diffs):.4f}s")

    # Analyze numeric columns
    print(f"\n📈 DATA COLUMN ANALYSIS:")

    # Sample first few records to show data structure
    print(f"\n  First 3 records (showing first 15 columns):")
    for i in range(min(3, len(rows))):
        print(f"    Record {i+1}: {rows[i][:15]}")

    # Analyze each column
    print(f"\n  Column value ranges:")
    num_cols = len(rows[0])
    for col_idx in range(2, min(20, num_cols)):  # Skip trial_id, config, show first 18 data cols
        try:
            values = [float(row[col_idx]) for row in rows if row[col_idx]]
            unique_count = len(set(values))

            if unique_count <= 5:
                print(f"    Column {col_idx} (likely flag/setting): unique values = {set(values)}")
            else:
                min_val = min(values)
                max_val = max(values)
                avg_val = sum(values) / len(values)
                print(f"    Column {col_idx}: min={min_val:.2f}, max={max_val:.2f}, avg={avg_val:.2f}, unique={unique_count}")
        except ValueError:
            print(f"    Column {col_idx}: non-numeric data")

    # Decode configuration
    config = rows[0][1].strip('"')
    print(f"\n🔍 CONFIGURATION DECODING:")
    print(f"  Raw config: {config}")
    print(f"\n  Possible interpretation:")
    parts = config.split('-')
    for part in parts:
        if part.startswith('u'):
            print(f"    • '{part}' - likely 'urban' scenario type")
        elif 's' in part and any(c.isdigit() for c in part):
            print(f"    • '{part}' - likely time parameter (seconds)")
        elif 'retr' in part.lower():
            print(f"    • '{part}' - likely 'retrieval' or 'retry' mechanism")
        elif part.isdigit():
            print(f"    • '{part}' - numeric parameter (distance/range?)")
        elif 'AHEAD' in part.upper():
            print(f"    • '{part}' - likely 'look-ahead' or forward sensor config")

    # Look for potential collision events (assuming zeros that change)
    print(f"\n🚗 POTENTIAL SIMULATION EVENTS:")

    # Check columns that are mostly zero but sometimes non-zero
    for col_idx in range(3, min(25, num_cols)):
        try:
            values = [float(row[col_idx]) for row in rows]
            zero_count = sum(1 for v in values if v == 0.0)
            nonzero_count = len(values) - zero_count

            if zero_count > len(values) * 0.7 and nonzero_count > 0:
                print(f"    Column {col_idx}: {nonzero_count} events detected (mostly zeros)")
                # Show when events happen
                event_times = [timestamps[i] for i, v in enumerate(values) if v != 0.0]
                if event_times:
                    print(f"      First event: {event_times[0]:.2f}s, Last event: {event_times[-1]:.2f}s")
        except ValueError:
            pass

    # Create summary report
    with open('simulation_summary.txt', 'w') as f:
        f.write("CARLA SIMULATION DATA RECOVERY REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"SIMULATION: CARLA v0.9.14 - Urban Driving Scenario\n\n")
        f.write(f"Trial ID: {rows[0][0]}\n")
        f.write(f"Configuration: {rows[0][1]}\n")
        f.write(f"Total records: {len(rows):,}\n")
        f.write(f"Duration: {max(timestamps) - min(timestamps):.2f} seconds\n")
        f.write(f"Sampling rate: ~{1/avg_timestep:.1f} Hz\n")
        f.write(f"Timestep: {avg_timestep:.4f} seconds\n\n")

        f.write("RECOVERED PARAMETERS:\n")
        f.write("-" * 70 + "\n")
        f.write(f"• Scenario type: Urban (from config)\n")
        f.write(f"• Number of vehicles: 10 (from README)\n")
        f.write(f"• CARLA version: 0.9.14\n")
        f.write(f"• Configuration string: {config}\n")
        f.write(f"• Data columns: {num_cols}\n")
        f.write(f"• Simulation start: {min(timestamps):.2f}s\n")
        f.write(f"• Simulation end: {max(timestamps):.2f}s\n\n")

        f.write("DATA STRUCTURE:\n")
        f.write("-" * 70 + "\n")
        f.write(f"Column 0: Trial ID\n")
        f.write(f"Column 1: Configuration string\n")
        f.write(f"Column 2: Timestamp\n")
        f.write(f"Columns 3-37: Sensor data, vehicle positions, collision events\n\n")

        f.write("TO RECONSTRUCT THE SIMULATION:\n")
        f.write("-" * 70 + "\n")
        f.write("1. Use CARLA v0.9.14\n")
        f.write("2. Set up urban driving scenario\n")
        f.write("3. Configure 10 autonomous vehicles\n")
        f.write(f"4. Use configuration: {config}\n")
        f.write(f"5. Set sampling rate to ~{1/avg_timestep:.1f} Hz\n")

    print(f"\n✓ Summary report saved to: simulation_summary.txt")

    print("\n" + "=" * 70)
    print("✓ Analysis complete!")
    print("=" * 70)
    print("\nNext steps to recover your simulation:")
    print("  1. Install CARLA 0.9.14")
    print("  2. Set up urban scenario with 10 vehicles")
    print(f"  3. Apply configuration: {config}")
    print(f"  4. Use ~{1/avg_timestep:.1f} Hz sampling rate")
    print("  5. The data contains position, sensor, and collision information")

if __name__ == '__main__':
    load_and_analyze_data()
