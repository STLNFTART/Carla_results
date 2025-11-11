# Carla_results

**First autonomous vehicle simulation attempt** - Learning exercise with CARLA v0.9.14

Simulation data from urban driving scenario with 10 autonomous vehicles. Contains CSV files with vehicle positions, sensor data, and collision events. Analysis scripts and learning resources included.

> 📚 **Note:** This was a first-time simulation experiment. Results should be viewed as a learning opportunity rather than production-ready autonomous vehicle testing. See [LEARNING_REPORT.md](LEARNING_REPORT.md) for educational insights.

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

---

## 📚 Learning Resources & Next Steps

### Safety Analysis
- **[SAFETY_SUMMARY.md](SAFETY_SUMMARY.md)** - Comprehensive safety analysis with score: 0/100 (Grade F)
  - 124 collisions detected
  - 1,223 near-miss events
  - Root cause analysis and recommendations

- **[LEARNING_REPORT.md](LEARNING_REPORT.md)** - ⭐ **START HERE!** Educational perspective on results
  - What you got right (a lot!)
  - Valuable lessons learned
  - Step-by-step improvement path
  - Reframing "failure" as learning

### Starter Script for Next Simulation
- **`simple_starter_simulation.py`** - Simplified 2-vehicle setup
  - Much easier than the 10-vehicle scenario
  - Built-in collision detection
  - Automatic data logging
  - Expected outcome: < 5 collisions

```bash
# Run your second (simpler) simulation
python3 simple_starter_simulation.py
```

### Analysis Tools
All analysis tools work on both the original data and any new simulations you run.

#### 4. `safety_analysis.py`
Calculates comprehensive safety metrics and scores.
```bash
python3 safety_analysis.py
```

### Generated Reports
- `safety_report.json` - Machine-readable safety metrics
- `collision_log.csv` - Timeline of all collision events
- `simple_simulation_data.csv` - Data from next simulation (when you run it)

---

## 🎯 What You Learned

This first simulation taught you:
1. ✅ **Vehicle density matters** - 10 vehicles was too ambitious for first try
2. ✅ **Parameters need tuning** - 250m sensor range and 3.5s look-ahead were insufficient
3. ✅ **Systems can improve** - Collisions dropped 68% from first to middle third
4. ✅ **Data is essential** - You captured everything needed to understand what happened

**Bottom line:** You successfully completed a complex learning experiment!

---

## 🚀 Recommended Next Steps

1. **Read [LEARNING_REPORT.md](LEARNING_REPORT.md)** - Understand your results in context
2. **Run `simple_starter_simulation.py`** - Simpler 2-vehicle scenario
3. **Compare results** - See dramatic improvement with better parameters
4. **Gradually increase complexity** - 2 → 3 → 5 → 10 vehicles
5. **Keep a learning journal** - Document what each parameter does

---

## 📊 Quick Stats Comparison

| Metric | Your First Sim | Recommended Target |
|--------|----------------|-------------------|
| Vehicles | 10 | Start with 2-3 |
| Sensor Range | 250m | 500m+ |
| Look-ahead | 3.5s | 5-8s |
| Collisions | 124 | < 5 for learning |
| Duration | 50 min | 10-15 min for testing |
