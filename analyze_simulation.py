#!/usr/bin/env python3
"""
Analyze CARLA simulation data to extract key information about the lost simulation.
This script helps recover metadata and visualize the simulation that generated the data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def load_data(filepath='Carla_Validation_.DATA'):
    """Load the CARLA simulation data."""
    # Define column names based on typical CARLA output structure
    columns = [
        'trial_id',
        'config',
        'timestamp',
        'col_3', 'col_4', 'col_5', 'col_6', 'col_7', 'col_8', 'col_9',
        'col_10', 'col_11', 'col_12', 'col_13', 'col_14', 'col_15', 'col_16',
        'col_17', 'col_18', 'col_19', 'col_20', 'col_21', 'col_22', 'col_23',
        'col_24', 'col_25', 'col_26', 'col_27', 'col_28', 'col_29', 'col_30',
        'col_31', 'col_32', 'col_33', 'col_34', 'col_35', 'col_36', 'col_37'
    ]

    df = pd.read_csv(filepath, header=None, names=columns)
    return df

def analyze_simulation(df):
    """Extract simulation metadata and statistics."""
    print("=" * 70)
    print("CARLA SIMULATION DATA ANALYSIS")
    print("=" * 70)

    # Basic info
    print("\n📊 BASIC INFORMATION:")
    print(f"  Trial ID: {df['trial_id'].iloc[0]}")
    print(f"  Configuration: {df['config'].iloc[0]}")
    print(f"  Total records: {len(df):,}")
    print(f"  Columns: {len(df.columns)}")

    # Time analysis
    print("\n⏱️  TIME ANALYSIS:")
    print(f"  Start time: {df['timestamp'].min():.2f}s")
    print(f"  End time: {df['timestamp'].max():.2f}s")
    print(f"  Duration: {df['timestamp'].max() - df['timestamp'].min():.2f}s")

    time_diffs = df['timestamp'].diff().dropna()
    print(f"  Average timestep: {time_diffs.mean():.4f}s")
    print(f"  Timestep std dev: {time_diffs.std():.6f}s")
    print(f"  Min timestep: {time_diffs.min():.4f}s")
    print(f"  Max timestep: {time_diffs.max():.4f}s")

    # Data statistics for numeric columns
    print("\n📈 DATA STATISTICS:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    print(f"\n  Columns with constant values (potential flags/settings):")
    for col in numeric_cols:
        unique_vals = df[col].nunique()
        if unique_vals <= 5:
            print(f"    {col}: {df[col].unique()}")

    print(f"\n  Columns with varying values (potential sensor/position data):")
    for col in numeric_cols:
        unique_vals = df[col].nunique()
        if unique_vals > 5:
            print(f"    {col}: min={df[col].min():.2f}, max={df[col].max():.2f}, "
                  f"mean={df[col].mean():.2f}, std={df[col].std():.2f}")

    return df

def decode_configuration(config_string):
    """Try to decode the configuration string."""
    print("\n🔍 CONFIGURATION DECODING:")
    print(f"  Raw config: {config_string}")
    print(f"\n  Possible interpretations:")
    print(f"    - 'u' might indicate: urban scenario")
    print(f"    - '3.5s' might indicate: 3.5 second parameter")
    print(f"    - 'retr' might indicate: retrieval/retry mechanism")
    print(f"    - '250' might indicate: 250 meter range or similar")
    print(f"    - 'cAHEAD' might indicate: 'look ahead' or forward sensor config")

def create_visualizations(df):
    """Create basic visualizations of the simulation data."""
    print("\n📊 Creating visualizations...")

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('CARLA Simulation Data Overview', fontsize=16)

    # Plot 1: Some numeric columns over time
    ax = axes[0, 0]
    numeric_cols = df.select_dtypes(include=[np.number]).columns[2:7]  # Skip timestamp
    for col in numeric_cols:
        if df[col].nunique() > 5:  # Only plot varying data
            ax.plot(df['timestamp'], df[col], alpha=0.7, label=col)
    ax.set_xlabel('Timestamp (s)')
    ax.set_ylabel('Value')
    ax.set_title('Selected Numeric Columns Over Time')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 2: More numeric columns
    ax = axes[0, 1]
    numeric_cols = df.select_dtypes(include=[np.number]).columns[7:12]
    for col in numeric_cols:
        if df[col].nunique() > 5:
            ax.plot(df['timestamp'], df[col], alpha=0.7, label=col)
    ax.set_xlabel('Timestamp (s)')
    ax.set_ylabel('Value')
    ax.set_title('Additional Numeric Columns Over Time')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 3: Data sampling rate
    ax = axes[1, 0]
    time_diffs = df['timestamp'].diff().dropna()
    ax.hist(time_diffs, bins=50, edgecolor='black', alpha=0.7)
    ax.set_xlabel('Time difference (s)')
    ax.set_ylabel('Frequency')
    ax.set_title('Sampling Rate Distribution')
    ax.grid(True, alpha=0.3)

    # Plot 4: Heatmap of correlation (sample of columns)
    ax = axes[1, 1]
    numeric_df = df.select_dtypes(include=[np.number]).iloc[:, :10]  # First 10 numeric
    corr = numeric_df.corr()
    im = ax.imshow(corr, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha='right')
    ax.set_yticklabels(corr.columns)
    ax.set_title('Correlation Matrix (First 10 Columns)')
    plt.colorbar(im, ax=ax)

    plt.tight_layout()
    plt.savefig('simulation_analysis.png', dpi=150, bbox_inches='tight')
    print(f"  ✓ Saved visualization to: simulation_analysis.png")

def export_summary(df):
    """Export a summary report."""
    with open('simulation_summary.txt', 'w') as f:
        f.write("CARLA SIMULATION DATA RECOVERY REPORT\n")
        f.write("=" * 70 + "\n\n")

        f.write(f"Trial ID: {df['trial_id'].iloc[0]}\n")
        f.write(f"Configuration: {df['config'].iloc[0]}\n")
        f.write(f"Total records: {len(df):,}\n")
        f.write(f"Duration: {df['timestamp'].max() - df['timestamp'].min():.2f}s\n")
        f.write(f"Sampling rate: ~{1/df['timestamp'].diff().mean():.1f} Hz\n\n")

        f.write("COLUMN SUMMARY:\n")
        f.write("-" * 70 + "\n")
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                f.write(f"{col}: min={df[col].min():.2f}, max={df[col].max():.2f}, "
                       f"mean={df[col].mean():.2f}\n")

    print(f"  ✓ Saved summary report to: simulation_summary.txt")

def main():
    """Main analysis function."""
    print("\nLoading CARLA simulation data...")
    df = load_data()

    # Analyze the data
    df = analyze_simulation(df)

    # Decode configuration
    config = df['config'].iloc[0]
    decode_configuration(config)

    # Create visualizations
    create_visualizations(df)

    # Export summary
    export_summary(df)

    print("\n" + "=" * 70)
    print("✓ Analysis complete!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - simulation_analysis.png (visualizations)")
    print("  - simulation_summary.txt (text summary)")
    print("\nNext steps to recover simulation:")
    print("  1. Check the configuration string for simulation parameters")
    print("  2. Analyze column patterns to identify sensor types")
    print("  3. Look for position/velocity data to reconstruct trajectories")
    print("  4. Check for collision events (zeros changing to non-zeros)")

if __name__ == '__main__':
    main()
