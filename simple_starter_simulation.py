#!/usr/bin/env python3
"""
Simple Starter Simulation - Your Second Attempt!

This is a much simpler setup than your first simulation.
Goal: Get 2 vehicles running safely for 10 minutes.

Expected outcome: < 5 collisions, building your confidence!
"""

import carla
import time
import csv
import sys

def run_simple_simulation():
    """Run a simple 2-vehicle simulation with improved parameters."""

    print("=" * 70)
    print("CARLA SIMPLE STARTER SIMULATION")
    print("=" * 70)
    print("\nGoal: 2 vehicles, 10 minutes, minimal collisions")
    print("This is a LEARNING exercise - focus on understanding the system\n")

    try:
        # Connect to CARLA
        print("Connecting to CARLA...")
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()
        print("✓ Connected!")

        # Configure world settings
        print("\nConfiguring simulation settings...")
        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.1  # 10 Hz - easier to manage
        world.apply_settings(settings)
        print("✓ Settings applied (10 Hz, synchronous mode)")

        # Get traffic manager
        traffic_manager = client.get_trafficmanager(8000)
        traffic_manager.set_global_distance_to_leading_vehicle(5.0)  # Safer distance
        traffic_manager.set_synchronous_mode(True)
        print("✓ Traffic manager configured (5.0m safe distance)")

        # Spawn 2 vehicles with good separation
        print("\nSpawning vehicles...")
        blueprint_library = world.get_blueprint_library()

        # Get a safe vehicle blueprint
        vehicle_blueprints = blueprint_library.filter('vehicle.tesla.model3')
        if not vehicle_blueprints:
            vehicle_blueprints = blueprint_library.filter('vehicle.*')

        vehicle_bp = vehicle_blueprints[0]

        # Get spawn points (pick ones far apart)
        spawn_points = world.get_map().get_spawn_points()
        if len(spawn_points) < 2:
            print("ERROR: Not enough spawn points on this map!")
            return

        # Spawn vehicle 1
        vehicle1 = world.spawn_actor(vehicle_bp, spawn_points[0])
        vehicle1.set_autopilot(True, 8000)
        print(f"✓ Vehicle 1 spawned at spawn point 0")

        # Spawn vehicle 2 far away (halfway through spawn points)
        spawn_point_2_idx = len(spawn_points) // 2
        vehicle2 = world.spawn_actor(vehicle_bp, spawn_points[spawn_point_2_idx])
        vehicle2.set_autopilot(True, 8000)
        print(f"✓ Vehicle 2 spawned at spawn point {spawn_point_2_idx} (well separated)")

        vehicles = [vehicle1, vehicle2]

        # Data collection setup
        print("\nStarting simulation...")
        print("Duration: 10 minutes (600 seconds)")
        print("Press Ctrl+C to stop early\n")

        data_log = []
        collision_count = 0
        start_time = time.time()

        # Collision sensor (optional - to detect collisions)
        def on_collision(event):
            nonlocal collision_count
            collision_count += 1

        collision_bp = blueprint_library.find('sensor.other.collision')
        collision_sensor1 = world.spawn_actor(collision_bp, carla.Transform(), attach_to=vehicle1)
        collision_sensor2 = world.spawn_actor(collision_bp, carla.Transform(), attach_to=vehicle2)
        collision_sensor1.listen(on_collision)
        collision_sensor2.listen(on_collision)

        # Main simulation loop
        simulation_time = 0.0
        duration = 600.0  # 10 minutes

        while simulation_time < duration:
            world.tick()

            # Collect data
            for i, vehicle in enumerate(vehicles):
                transform = vehicle.get_transform()
                velocity = vehicle.get_velocity()

                data_log.append({
                    'timestamp': simulation_time,
                    'vehicle_id': i,
                    'x': transform.location.x,
                    'y': transform.location.y,
                    'z': transform.location.z,
                    'yaw': transform.rotation.yaw,
                    'vx': velocity.x,
                    'vy': velocity.y,
                    'vz': velocity.z,
                })

            # Progress update every 10 seconds
            if int(simulation_time) % 10 == 0 and simulation_time > 0:
                elapsed = time.time() - start_time
                progress = (simulation_time / duration) * 100
                print(f"  [{int(progress):3d}%] Time: {simulation_time:.1f}s | "
                      f"Collisions: {collision_count} | "
                      f"Real time: {elapsed:.1f}s")

            simulation_time += 0.1

        # Cleanup
        print("\n✓ Simulation complete!")
        print(f"\nCleaning up...")
        collision_sensor1.destroy()
        collision_sensor2.destroy()
        vehicle1.destroy()
        vehicle2.destroy()

        # Reset to asynchronous mode
        settings.synchronous_mode = False
        world.apply_settings(settings)

        # Save data
        print("\nSaving data...")
        with open('simple_simulation_data.csv', 'w') as f:
            if data_log:
                writer = csv.DictWriter(f, fieldnames=data_log[0].keys())
                writer.writeheader()
                writer.writerows(data_log)
        print(f"✓ Saved {len(data_log)} data points to: simple_simulation_data.csv")

        # Results
        print("\n" + "=" * 70)
        print("SIMULATION RESULTS")
        print("=" * 70)
        print(f"Duration: {duration:.1f} seconds")
        print(f"Vehicles: 2")
        print(f"Data points: {len(data_log):,}")
        print(f"Collisions: {collision_count}")

        if collision_count == 0:
            print("\n🎉 PERFECT! No collisions detected!")
            print("You're ready to try 3-4 vehicles next.")
        elif collision_count < 5:
            print("\n✓ GOOD! Very few collisions.")
            print("Try adjusting parameters and running again.")
        elif collision_count < 20:
            print("\n⚠️  MODERATE collision count.")
            print("Review the data and try increasing safe distance.")
        else:
            print("\n⚠️  HIGH collision count.")
            print("Consider reducing simulation duration or checking spawn points.")

        print("\nNext steps:")
        print("  1. Analyze simple_simulation_data.csv")
        print("  2. Compare to your first simulation")
        print("  3. Try adjusting traffic_manager.set_global_distance_to_leading_vehicle()")
        print("  4. Gradually increase vehicle count: 3, then 4, then 5...")
        print("=" * 70)

    except KeyboardInterrupt:
        print("\n\nSimulation stopped by user")
        # Cleanup
        try:
            vehicle1.destroy()
            vehicle2.destroy()
            collision_sensor1.destroy()
            collision_sensor2.destroy()
        except:
            pass

    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure CARLA server is running: ./CarlaUE4.sh")
        print("  2. Check that port 2000 is not blocked")
        print("  3. Verify you have CARLA 0.9.14 or compatible version")
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(run_simple_simulation())
