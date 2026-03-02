"""
Update CSV files and generate plots with Level 2 molecules
"""
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

print("="*80)
print("📊 UPDATING DATA WITH LEVEL 2 MOLECULES")
print("="*80)

# Load existing core analysis
with open('results/core_analysis.json', 'r') as f:
    core_data = json.load(f)

# Load level 2 analysis
with open('results/level2_analysis.json', 'r') as f:
    level2_data = json.load(f)

# Combine data
all_data = {**core_data, **level2_data}

# 1) Update molecular_summary.csv
print("\n1️⃣  Updating molecular_summary.csv...")
summary_rows = []

for mol in ['H2', 'CO', 'H2O', 'NH3', 'CH4']:
    if mol in all_data:
        data = all_data[mol]
        
        if mol == 'H2':
            summary_rows.append({
                'molecule': mol,
                'bond_type': 'H-H',
                'bond_calc_A': data['geometry']['bond_length'],
                'bond_exp_A': data['geometry']['exp_bond'],
                'bond_error_pct': data['geometry']['error_pct']
            })
        elif mol == 'CO':
            summary_rows.append({
                'molecule': mol,
                'bond_type': 'C-O',
                'bond_calc_A': data['geometry']['bond_length'],
                'bond_exp_A': data['geometry']['exp_bond'],
                'bond_error_pct': data['geometry']['error_pct']
            })
        elif mol == 'H2O':
            summary_rows.append({
                'molecule': mol,
                'bond_type': 'O-H',
                'bond_calc_A': data['geometry']['oh_bond_avg'],
                'bond_exp_A': data['geometry']['exp_bond'],
                'bond_error_pct': data['geometry']['bond_error_pct']
            })
        elif mol == 'NH3':
            summary_rows.append({
                'molecule': mol,
                'bond_type': 'N-H',
                'bond_calc_A': data['geometry']['nh_avg'],
                'bond_exp_A': data['geometry']['nh_exp'],
                'bond_error_pct': data['geometry']['bond_error_pct']
            })
        elif mol == 'CH4':
            summary_rows.append({
                'molecule': mol,
                'bond_type': 'C-H',
                'bond_calc_A': data['geometry']['ch_avg'],
                'bond_exp_A': data['geometry']['ch_exp'],
                'bond_error_pct': data['geometry']['bond_error_pct']
            })

df_summary = pd.DataFrame(summary_rows)
df_summary.to_csv('results/molecular_summary.csv', index=False)
print(f"   ✅ Saved molecular_summary.csv ({len(df_summary)} molecules)")

# 2) Update electronic_properties.csv
print("\n2️⃣  Creating electronic_properties.csv...")
elec_rows = []

for mol in ['H2', 'CO', 'H2O', 'NH3', 'CH4']:
    if mol in all_data:
        data = all_data[mol]
        elec_rows.append({
            'molecule': mol,
            'homo_eV': data['electronic']['homo_eV'],
            'lumo_eV': data['electronic']['lumo_eV'],
            'gap_eV': data['electronic']['gap_eV'],
            'gap_exp_eV': data['electronic']['exp_gap'],
            'gap_error_pct': data['electronic']['gap_error_pct']
        })

df_elec = pd.DataFrame(elec_rows)
df_elec.to_csv('results/electronic_properties.csv', index=False)
print(f"   ✅ Saved electronic_properties.csv ({len(df_elec)} molecules)")

# 3) Update dipole_moments.csv
print("\n3️⃣  Creating dipole_moments.csv...")
dipole_rows = []

for mol in ['H2', 'CO', 'H2O', 'NH3', 'CH4']:
    if mol in all_data:
        data = all_data[mol]
        row = {
            'molecule': mol,
            'dipole_calc_D': data['dipole']['dipole_D'],
            'dipole_exp_D': data['dipole']['exp_dipole_D']
        }
        if 'error_pct' in data['dipole']:
            row['error_pct'] = data['dipole']['error_pct']
        else:
            row['error_pct'] = 0.0
        dipole_rows.append(row)

df_dipole = pd.DataFrame(dipole_rows)
df_dipole.to_csv('results/dipole_moments.csv', index=False)
print(f"   ✅ Saved dipole_moments.csv ({len(df_dipole)} molecules)")

# 4) Generate updated plots
print("\n4️⃣  Generating updated plots...")

molecules = ['H2', 'CO', 'H2O', 'NH3', 'CH4']
labels = ['H₂', 'CO', 'H₂O', 'NH₃', 'CH₄']
colors = ['#2E7D32', '#1976D2', '#C62828', '#FF6F00', '#9C27B0']

# Plot 1: HOMO-LUMO Gaps
fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')

gaps_calc = []
gaps_exp = []
errors = []

for mol in molecules:
    if mol in all_data:
        data = all_data[mol]
        gaps_calc.append(data['electronic']['gap_eV'])
        gaps_exp.append(data['electronic']['exp_gap'])
        errors.append(data['electronic']['gap_error_pct'])

x = np.arange(len(molecules))
width = 0.35

bars1 = ax.bar(x - width/2, gaps_calc, width, label='DFT-PBE (GGA)', 
               color=colors, edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x + width/2, gaps_exp, width, label='Experimental',
               color='lightgray', edgecolor='black', linewidth=1.5, hatch='//')

# Add error annotations
for i, (bar, err) in enumerate(zip(bars1, errors)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 0.3,
            f'{err:.1f}%', ha='center', va='bottom', fontsize=9,
            fontweight='bold', color='red')

ax.set_ylabel('HOMO-LUMO Gap (eV)', fontsize=12, fontweight='bold')
ax.set_title('HOMO-LUMO Gaps (Level 1 + Level 2)', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=12, fontweight='bold')
ax.legend(fontsize=11, frameon=True, edgecolor='black')
ax.grid(True, axis='y', alpha=0.2, linestyle=':')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add GGA note
ax.text(0.98, 0.98, 'Note: GGA (PBE) typically\nunderestimates gaps',
        transform=ax.transAxes, fontsize=9, va='top', ha='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('plots/homo_lumo_gaps_all.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("   ✅ homo_lumo_gaps_all.png")

# Plot 2: Dipole Moments
fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')

dipoles_calc = []
dipoles_exp = []
errors_dip = []

for mol in molecules:
    if mol in all_data:
        data = all_data[mol]
        dipoles_calc.append(data['dipole']['dipole_D'])
        dipoles_exp.append(data['dipole']['exp_dipole_D'])
        if 'error_pct' in data['dipole']:
            errors_dip.append(data['dipole']['error_pct'])
        else:
            errors_dip.append(0)

x = np.arange(len(molecules))
width = 0.35

bars1 = ax.bar(x - width/2, dipoles_calc, width, label='DFT-PBE', 
               color=colors, edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x + width/2, dipoles_exp, width, label='Experimental',
               color='lightgray', edgecolor='black', linewidth=1.5, hatch='//')

# Add error annotations
for i, (bar, err) in enumerate(zip(bars1, errors_dip)):
    if err > 0:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.05,
                f'{err:.1f}%', ha='center', va='bottom', fontsize=9,
                fontweight='bold', color='red')

ax.set_ylabel('Dipole Moment (D)', fontsize=12, fontweight='bold')
ax.set_title('Dipole Moments (Level 1 + Level 2)', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=12, fontweight='bold')
ax.legend(fontsize=11, frameon=True, edgecolor='black')
ax.grid(True, axis='y', alpha=0.2, linestyle=':')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add symmetry check note
ax.text(0.98, 0.98, 'Symmetry check:\nH₂, CH₄ dipole ≈ 0 ✓',
        transform=ax.transAxes, fontsize=9, va='top', ha='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8))

plt.tight_layout()
plt.savefig('plots/dipole_moments_all.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("   ✅ dipole_moments_all.png")

print("\n✅ All data and plots updated with Level 2 molecules")

