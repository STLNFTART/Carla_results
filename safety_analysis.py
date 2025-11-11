#!/usr/bin/env python3
"""
Safety Analysis for CARLA Simulation Data
Calculates safety scores and metrics from the simulation run.
"""

import csv
from collections import defaultdict
import json

def analyze_safety(filepath='Carla_Validation_.DATA'):
    """Comprehensive safety analysis of CARLA simulation."""

    print("=" * 70)
    print("CARLA SIMULATION SAFETY ANALYSIS")
    print("=" * 70)

    # Load data
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Extract key metrics
    timestamps = []
    collision_events = []
    near_miss_events = []

    # Track various safety metrics
    velocity_violations = 0
    sudden_changes = 0

    # Event columns (16-17 show binary flags, 20-22 show sporadic events)
    for i, row in enumerate(rows):
        try:
            timestamp = float(row[2])
            timestamps.append(timestamp)

            # Collision indicators (columns 16-17)
            collision_flag_1 = float(row[16]) if len(row) > 16 else 0.0
            collision_flag_2 = float(row[17]) if len(row) > 17 else 0.0

            # Additional event columns (20-22)
            event_col_20 = float(row[20]) if len(row) > 20 else 0.0
            event_col_21 = float(row[21]) if len(row) > 21 else 0.0
            event_col_22 = float(row[22]) if len(row) > 22 else 0.0

            # Detect collision events
            if collision_flag_1 > 0 or collision_flag_2 > 0:
                collision_events.append({
                    'timestamp': timestamp,
                    'severity': max(collision_flag_1, collision_flag_2),
                    'type': 'collision'
                })

            # Detect near-miss events (columns 20-22 that are usually zero)
            if event_col_20 > 0 or event_col_21 > 0 or event_col_22 > 0:
                near_miss_events.append({
                    'timestamp': timestamp,
                    'values': [event_col_20, event_col_21, event_col_22]
                })

            # Check for sudden changes in position (potential dangerous maneuvers)
            if i > 0:
                prev_pos_x = float(rows[i-1][5])
                prev_pos_y = float(rows[i-1][6])
                curr_pos_x = float(row[5])
                curr_pos_y = float(row[6])

                distance = ((curr_pos_x - prev_pos_x)**2 + (curr_pos_y - prev_pos_y)**2)**0.5
                time_diff = timestamp - float(rows[i-1][2])

                if time_diff > 0:
                    instantaneous_speed = distance / time_diff
                    # Flag very high speeds (threshold: 10000 units/s as anomaly)
                    if instantaneous_speed > 10000:
                        sudden_changes += 1

        except (ValueError, IndexError):
            continue

    # Calculate safety metrics
    total_duration = max(timestamps) - min(timestamps)
    total_records = len(rows)
    num_vehicles = 10  # From README

    # Collision rate (per vehicle per hour)
    num_collisions = len(collision_events)
    hours = total_duration / 3600.0
    collision_rate = num_collisions / (num_vehicles * hours) if hours > 0 else 0

    # Near-miss rate
    num_near_misses = len(near_miss_events)
    near_miss_rate = num_near_misses / (num_vehicles * hours) if hours > 0 else 0

    # Mean time between failures (MTBF)
    if num_collisions > 0:
        mtbf = total_duration / num_collisions
    else:
        mtbf = total_duration

    # Calculate safety score (0-100 scale)
    # Higher score = safer
    base_score = 100.0

    # Deductions
    collision_penalty = min(num_collisions * 2.0, 50)  # Up to 50 points
    near_miss_penalty = min(num_near_misses * 0.5, 30)  # Up to 30 points
    rate_penalty = min(collision_rate * 10, 20)  # Up to 20 points

    safety_score = max(base_score - collision_penalty - near_miss_penalty - rate_penalty, 0)

    # Determine safety grade
    if safety_score >= 90:
        grade = "A (Excellent)"
    elif safety_score >= 80:
        grade = "B (Good)"
    elif safety_score >= 70:
        grade = "C (Acceptable)"
    elif safety_score >= 60:
        grade = "D (Poor)"
    else:
        grade = "F (Unsafe)"

    # Print results
    print(f"\n📊 SIMULATION OVERVIEW:")
    print(f"  Duration: {total_duration:.1f} seconds ({total_duration/3600:.2f} hours)")
    print(f"  Number of vehicles: {num_vehicles}")
    print(f"  Total data points: {total_records:,}")

    print(f"\n⚠️  SAFETY EVENTS:")
    print(f"  Total collisions: {num_collisions}")
    print(f"  Near-miss events: {num_near_misses}")
    print(f"  Total safety events: {num_collisions + num_near_misses}")
    print(f"  Sudden maneuvers: {sudden_changes}")

    print(f"\n📈 SAFETY RATES:")
    print(f"  Collision rate: {collision_rate:.2f} per vehicle per hour")
    print(f"  Near-miss rate: {near_miss_rate:.2f} per vehicle per hour")
    print(f"  Mean time between collisions: {mtbf:.1f} seconds ({mtbf/60:.1f} minutes)")

    print(f"\n🎯 SAFETY SCORE: {safety_score:.1f}/100")
    print(f"  Grade: {grade}")
    print(f"\n  Score breakdown:")
    print(f"    Base score: 100.0")
    print(f"    Collision penalty: -{collision_penalty:.1f}")
    print(f"    Near-miss penalty: -{near_miss_penalty:.1f}")
    print(f"    Rate penalty: -{rate_penalty:.1f}")
    print(f"    Final score: {safety_score:.1f}")

    # Collision timeline
    if collision_events:
        print(f"\n🚗 COLLISION TIMELINE:")
        collision_times = [e['timestamp'] for e in collision_events]
        print(f"  First collision: {min(collision_times):.1f}s")
        print(f"  Last collision: {max(collision_times):.1f}s")
        print(f"  Collision concentration: {len([t for t in collision_times if t > 2000])}/{num_collisions} in second half")

    # Time-based analysis
    print(f"\n⏱️  TEMPORAL ANALYSIS:")
    early_collisions = len([e for e in collision_events if e['timestamp'] < total_duration/3 + min(timestamps)])
    mid_collisions = len([e for e in collision_events if total_duration/3 + min(timestamps) <= e['timestamp'] < 2*total_duration/3 + min(timestamps)])
    late_collisions = len([e for e in collision_events if e['timestamp'] >= 2*total_duration/3 + min(timestamps)])

    print(f"  First third: {early_collisions} collisions")
    print(f"  Middle third: {mid_collisions} collisions")
    print(f"  Final third: {late_collisions} collisions")

    # Safety recommendations
    print(f"\n💡 SAFETY INSIGHTS:")
    if num_collisions > 50:
        print(f"  ⚠️  HIGH collision count detected")
        print(f"     → Review vehicle control algorithms")
        print(f"     → Check sensor detection ranges")
    elif num_collisions > 20:
        print(f"  ⚠️  MODERATE collision count")
        print(f"     → Consider increasing safety margins")
    else:
        print(f"  ✓ Collision count is relatively low")

    if collision_rate > 10:
        print(f"  ⚠️  HIGH collision rate per vehicle")
        print(f"     → Review path planning algorithms")
    elif collision_rate > 5:
        print(f"  ⚠️  MODERATE collision rate")
        print(f"     → Optimize vehicle spacing")
    else:
        print(f"  ✓ Collision rate is acceptable")

    if near_miss_rate > 50:
        print(f"  ⚠️  HIGH near-miss rate")
        print(f"     → Vehicles frequently in risky situations")
        print(f"     → Review detection and avoidance systems")
    elif near_miss_rate > 20:
        print(f"  ⚠️  MODERATE near-miss rate")
        print(f"     → Consider more conservative driving parameters")

    if late_collisions > early_collisions:
        print(f"  ⚠️  Collisions INCREASING over time")
        print(f"     → Possible system degradation or traffic buildup")
    elif early_collisions > late_collisions:
        print(f"  ✓ Collisions DECREASING over time (system learning/stabilizing)")

    # Save detailed report
    report = {
        'simulation': {
            'trial_id': 'MOVE-TRIALT148',
            'configuration': 'u-3.5s-retr-250-cAHEAD',
            'duration_seconds': total_duration,
            'num_vehicles': num_vehicles
        },
        'safety_score': {
            'overall_score': round(safety_score, 1),
            'grade': grade,
            'breakdown': {
                'base': 100.0,
                'collision_penalty': round(collision_penalty, 1),
                'near_miss_penalty': round(near_miss_penalty, 1),
                'rate_penalty': round(rate_penalty, 1)
            }
        },
        'events': {
            'total_collisions': num_collisions,
            'total_near_misses': num_near_misses,
            'sudden_maneuvers': sudden_changes
        },
        'rates': {
            'collision_rate_per_vehicle_per_hour': round(collision_rate, 2),
            'near_miss_rate_per_vehicle_per_hour': round(near_miss_rate, 2),
            'mean_time_between_collisions_seconds': round(mtbf, 1)
        },
        'temporal_distribution': {
            'first_third': early_collisions,
            'middle_third': mid_collisions,
            'final_third': late_collisions
        }
    }

    with open('safety_report.json', 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n✓ Detailed safety report saved to: safety_report.json")

    # Generate collision event log
    with open('collision_log.csv', 'w') as f:
        f.write('timestamp,event_type,severity\n')
        for event in sorted(collision_events + near_miss_events, key=lambda x: x['timestamp']):
            event_type = event.get('type', 'near_miss')
            severity = event.get('severity', 'N/A')
            f.write(f"{event['timestamp']:.2f},{event_type},{severity}\n")

    print(f"✓ Collision log saved to: collision_log.csv")

    print("\n" + "=" * 70)

    return safety_score, report

if __name__ == '__main__':
    score, report = analyze_safety()
    print(f"\n🎯 FINAL SAFETY SCORE: {score:.1f}/100")
    print("=" * 70)
