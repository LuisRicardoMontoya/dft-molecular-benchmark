"""
Generate convergence plot from BFGS history CSV files
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os

molecules = ['H2', 'CO', 'H2O']
labels = ['H₂', 'CO', 'H₂O']
colors_mol = ['#2E7D32', '#1976D2', '#C62828']

# Count how many molecules have history
available = []
for mol in molecules:
    csv_path = f'runs/{mol}/bfgs_history.csv'
    if os.path.exists(csv_path):
        available.append(mol)

if len(available) == 0:
    print("❌ No BFGS history files found")
    exit(1)

# Create figure with appropriate number of subplots
n_plots = len(available)
fig, axes = plt.subplots(n_plots, 1, figsize=(12, 5*n_plots), facecolor='white')

if n_plots == 1:
    axes = [axes]

for idx, mol in enumerate(available):
    ax = axes[idx]
    mol_idx = molecules.index(mol)
    
    # Read history
    df = pd.read_csv(f'runs/{mol}/bfgs_history.csv')
    
    steps = df['iteration'].values
    energies = df['energy_eV'].values
    fmax = df['fmax_eV_A'].values
    
    # Normalize energy to first step
    energies_rel = energies - energies[0]
    
    # Plot energy (left axis)
    ax1 = ax
    line1 = ax1.plot(steps, energies_rel, 'o-', color=colors_mol[mol_idx], 
                    linewidth=2, markersize=8, markeredgecolor='black',
                    markeredgewidth=1, label='Energy change', zorder=3)
    ax1.set_xlabel('Optimization Step', fontsize=12, fontweight='bold')
    ax1.set_ylabel('ΔE (eV)', fontsize=12, fontweight='bold', color=colors_mol[mol_idx])
    ax1.tick_params(axis='y', labelcolor=colors_mol[mol_idx])
    
    # Plot forces (right axis)
    ax2 = ax1.twinx()
    line2 = ax2.plot(steps, fmax, 's--', color='#FF6F00', 
                    linewidth=2, markersize=7, markeredgecolor='black',
                    markeredgewidth=1, label='Max force', zorder=2)
    ax2.axhline(0.02, color='red', linestyle=':', linewidth=2, 
               alpha=0.7, label='Convergence (0.02 eV/Å)', zorder=1)
    ax2.set_ylabel('Max Force (eV/Å)', fontsize=12, fontweight='bold', color='#FF6F00')
    ax2.tick_params(axis='y', labelcolor='#FF6F00')
    
    # Title
    ax1.set_title(f'{labels[mol_idx]} - BFGS Optimization', 
                 fontsize=13, fontweight='bold', pad=10)
    
    # Combined legend
    lines = line1 + line2 + [ax2.lines[-1]]
    labs = [l.get_label() for l in lines]
    ax1.legend(lines, labs, loc='upper right', fontsize=10, 
              frameon=True, edgecolor='black')
    
    # Grid
    ax1.grid(True, alpha=0.2, linestyle=':', linewidth=0.5)
    ax2.grid(False)
    
    # Spines
    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    
    # Convergence annotation
    if fmax[-1] < 0.02:
        ax2.text(0.98, 0.02, f'✓ Converged\n({len(steps)-1} steps)',
                transform=ax2.transAxes, fontsize=10, fontweight='bold',
                ha='right', va='bottom', color='green',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='lightgreen', 
                         edgecolor='green', alpha=0.7))

# Note for missing molecules
missing = set(molecules) - set(available)
if missing:
    note = f"Note: Convergence history not recorded for: {', '.join(missing)}"
    fig.text(0.5, 0.01, note, ha='center', fontsize=10, style='italic')

plt.tight_layout()
plt.savefig('plots/convergence_analysis_pub.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print(f"✅ Convergence plot generated for {len(available)} molecules")
if missing:
    print(f"⚠️  Missing history for: {', '.join(missing)}")

