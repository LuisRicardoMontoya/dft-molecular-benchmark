"""
Generate CORE plots for all molecules
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import numpy as np

# Load core analysis
with open('results/core_analysis.json', 'r') as f:
    data = json.load(f)

molecules = ['H2', 'CO', 'H2O']
labels = ['H₂', 'CO', 'H₂O']
colors = ['#2E7D32', '#1976D2', '#C62828']

# =====================================================================
# FIGURE 1: Molecular Orbital Diagrams (3 panels)
# =====================================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 6), facecolor='white')

for idx, mol in enumerate(molecules):
    ax = axes[idx]
    elec = data[mol]['electronic']
    
    homo = elec['homo_eV']
    lumo = elec['lumo_eV']
    gap = elec['gap_eV']
    
    # Plot HOMO and LUMO
    ax.hlines(homo, 0, 1, colors=colors[idx], linewidth=4, label='HOMO')
    ax.hlines(lumo, 0, 1, colors='orange', linewidth=4, label='LUMO', linestyle='--')
    
    # Gap annotation
    ax.annotate('', xy=(1.2, homo), xytext=(1.2, lumo),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text(1.4, (homo + lumo) / 2, f'{gap:.2f} eV',
            fontsize=11, va='center', fontweight='bold')
    
    # Labels
    ax.text(0.5, homo, 'HOMO', ha='center', va='top', fontsize=10, 
            fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[idx], alpha=0.8))
    ax.text(0.5, lumo, 'LUMO', ha='center', va='bottom', fontsize=10,
            fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='orange', alpha=0.8))
    
    # Styling
    ax.set_xlim(-0.2, 1.8)
    ax.set_ylim(min(homo, lumo) - 2, max(homo, lumo) + 2)
    ax.set_ylabel('Energy (eV)', fontsize=12, fontweight='bold')
    ax.set_title(f'{labels[idx]} Orbitals', fontsize=13, fontweight='bold')
    ax.set_xticks([])
    ax.grid(True, axis='y', alpha=0.2, linestyle=':')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

plt.tight_layout()
plt.savefig('plots/molecular_orbitals_core.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ molecular_orbitals_core.png")

# =====================================================================
# FIGURE 2: Dipole Moments Comparison
# =====================================================================
fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')

dipoles_calc = []
dipoles_exp = []
errors = []

for mol in molecules:
    dip = data[mol]['dipole']
    dipoles_calc.append(dip['dipole_D'])
    dipoles_exp.append(dip.get('exp_dipole_D', 0))
    if 'error_pct' in dip:
        errors.append(dip['error_pct'])
    else:
        errors.append(0)

x = np.arange(len(molecules))
width = 0.35

bars1 = ax.bar(x - width/2, dipoles_calc, width, label='DFT-PBE', 
               color=colors, edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x + width/2, dipoles_exp, width, label='Experimental',
               color='lightgray', edgecolor='black', linewidth=1.5, hatch='//')

# Add error annotations
for i, (bar, err) in enumerate(zip(bars1, errors)):
    if err > 0:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.05,
                f'{err:.1f}%', ha='center', va='bottom', fontsize=9,
                fontweight='bold', color='red')

ax.set_ylabel('Dipole Moment (D)', fontsize=12, fontweight='bold')
ax.set_title('Dipole Moments Comparison', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=12, fontweight='bold')
ax.legend(fontsize=11, frameon=True, edgecolor='black')
ax.grid(True, axis='y', alpha=0.2, linestyle=':')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('plots/dipole_moments_core.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ dipole_moments_core.png")

# =====================================================================
# FIGURE 3: Geometry Summary Table (as image)
# =====================================================================
fig, ax = plt.subplots(figsize=(12, 4), facecolor='white')
ax.axis('off')

table_data = []
table_data.append(['Molecule', 'Property', 'DFT-PBE', 'Experimental', 'Error (%)'])

for idx, mol in enumerate(molecules):
    geom = data[mol]['geometry']
    if mol == 'H2':
        table_data.append([labels[idx], 'Bond (Å)', f"{geom['bond_length']:.4f}", 
                          f"{geom['exp_bond']:.4f}", f"{geom['error_pct']:.2f}"])
    elif mol == 'CO':
        table_data.append([labels[idx], 'C-O Bond (Å)', f"{geom['bond_length']:.4f}",
                          f"{geom['exp_bond']:.4f}", f"{geom['error_pct']:.2f}"])
    elif mol == 'H2O':
        table_data.append([labels[idx], 'O-H Bond (Å)', f"{geom['oh_bond_avg']:.4f}",
                          f"{geom['exp_bond']:.4f}", f"{geom['bond_error_pct']:.2f}"])
        table_data.append(['', 'H-O-H Angle (°)', f"{geom['hoh_angle']:.2f}",
                          f"{geom['exp_angle']:.2f}", f"{geom['angle_error_pct']:.2f}"])

table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.15, 0.25, 0.2, 0.2, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2.5)

# Style header
for i in range(5):
    table[(0, i)].set_facecolor('#2E7D32')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style rows
for i in range(1, len(table_data)):
    for j in range(5):
        if j == 4:  # Error column
            table[(i, j)].set_facecolor('#FFE6E6')
        else:
            table[(i, j)].set_facecolor('#F5F5F5' if i % 2 == 0 else 'white')

plt.title('Optimized Geometries - Summary', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('plots/geometry_summary_core.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ geometry_summary_core.png")

print("\n✅ All core plots generated")
