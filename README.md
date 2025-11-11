# Carla_results

Simulation data from CARLA v0.9.14 for urban driving scenario with 10 autonomous vehicles. Contains CSV files with vehicle positions, sensor data, and collision events. Analysis scripts included.

## Recovered Simulation Details

**Trial ID:** MOVE-TRIALT148
**Configuration:** u-3.5s-retr-250-cAHEAD
**Duration:** 3,032.6 seconds (~50.5 minutes)
**Sampling Rate:** ~5.6 Hz (0.179s timestep)
**Total Records:** 6,129 data points
**Events Detected:** 124 collision/event occurrences

### Configuration Breakdown
- **u** - Urban scenario type
- **3.5s** - 3.5 second look-ahead time parameter
- **retr-250** - Retrieval mechanism with 250m range
- **cAHEAD** - Forward-looking sensor configuration

### Data Files
- `Carla_Validation_.DATA` - Main simulation data (38 columns)
- `trajectories.csv` - Extracted vehicle trajectories (generated)
- `events.csv` - Extracted collision/event data (generated)
- `simulation_summary.txt` - Detailed analysis report (generated)

### Analysis Tools

#### 1. `analyze_simulation_simple.py`
Analyzes the raw CARLA data and generates a comprehensive report.
```bash
python3 analyze_simulation_simple.py
```

#### 2. `extract_trajectories.py`
Extracts vehicle trajectories and events into separate CSV files.
```bash
python3 extract_trajectories.py
```

#### 3. `recreate_simulation.py`
Provides instructions and template code for recreating the simulation.
```bash
python3 recreate_simulation.py
```

### Data Structure (38 columns)
- **Column 0:** Trial ID
- **Column 1:** Configuration string
- **Column 2:** Timestamp (seconds)
- **Column 3:** Heading/orientation (~12°)
- **Column 4:** Angle data (0-360°)
- **Columns 5-11:** Position/coordinate data (194-5201 range)
- **Columns 12-15:** Velocity/acceleration data (-321 to 334 range)
- **Columns 16-17:** Event flags (collision indicators)
- **Columns 18-19:** State flags
- **Columns 20-37:** Additional sensor and vehicle data

### Key Findings
- **Total Distance Traveled:** ~1,401,805 units
- **Average Heading:** 12.19 degrees
- **Event Occurrences:** 124 detected events across the simulation
- **Position Range:** X: 194-5201, Y: 196-5201

### To Recreate This Simulation
1. Install CARLA 0.9.14
2. Set up urban driving scenario (Town01/Town03/Town05)
3. Configure 10 autonomous vehicles with autopilot
4. Apply configuration: `u-3.5s-retr-250-cAHEAD`
5. Set sampling rate to 5.6 Hz (0.179s fixed delta)
6. Enable data logging for positions, sensors, and collision events

See `recreate_simulation.py` for detailed setup instructions and Python template code.
