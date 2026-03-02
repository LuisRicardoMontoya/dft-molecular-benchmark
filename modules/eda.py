"""EDA and plotting"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def generate_all_plots():
    print("\n📈 Generating EDA plots...")
    
    # Load data
    mol_summary = pd.read_csv('results/molecular_summary.csv')
    elec_props = pd.read_csv('results/electronic_properties.csv')
    
    # Gap bar chart
    plt.figure(figsize=(8,6))
    plt.bar(elec_props['molecule'], elec_props['gap_eV'], color='#3498db', alpha=0.8, edgecolor='black')
    plt.ylabel('HOMO-LUMO Gap (eV)', fontweight='bold')
    plt.title('Electronic Band Gap', fontweight='bold', fontsize=13)
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('plots/gap_bar.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Dipole bar chart
    plt.figure(figsize=(8,6))
    plt.bar(elec_props['molecule'], elec_props['dipole_D'], color='#e74c3c', alpha=0.8, edgecolor='black')
    plt.ylabel('Dipole Moment (D)', fontweight='bold')
    plt.title('Molecular Dipole Moments', fontweight='bold', fontsize=13)
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('plots/dipole_bar.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Scatter dipole vs gap
    plt.figure(figsize=(8,6))
    plt.scatter(elec_props['gap_eV'], elec_props['dipole_D'], s=100, color='#9b59b6', edgecolor='black')
    for _, row in elec_props.iterrows():
        plt.annotate(row['molecule'], (row['gap_eV'], row['dipole_D']), 
                    xytext=(5,5), textcoords='offset points', fontsize=10)
    plt.xlabel('HOMO-LUMO Gap (eV)', fontweight='bold')
    plt.ylabel('Dipole Moment (D)', fontweight='bold')
    plt.title('Gap vs Dipole', fontweight='bold', fontsize=13)
    plt.grid(True, alpha=0.3)
    plt.savefig('plots/dipole_vs_gap_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Plots generated: gap_bar, dipole_bar, dipole_vs_gap_scatter")

