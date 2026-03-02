"""H2 bond scan"""
import csv, numpy as np
from ase import Atoms
from gpaw import GPAW
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def run_h2_scan(metadata):
    params = metadata['dft_parameters']
    scan_params = metadata['h2_scan']
    
    R_vals = np.linspace(scan_params['R_min'], scan_params['R_max'], scan_params['n_points'])
    results = []
    
    print(f"\n⚡ Scanning {len(R_vals)} points...")
    
    for i, R in enumerate(R_vals):
        atoms = Atoms('H2', positions=[[0,0,0], [R,0,0]])
        atoms.center(vacuum=params['vacuum'])
        atoms.set_pbc(True)
        
        calc = GPAW(mode='fd', xc='PBE', h=params['grid_spacing'], txt=None)
        atoms.calc = calc
        
        E = atoms.get_potential_energy()
        results.append({'R_A': R, 'E_eV': E})
        print(f"   [{i+1}/{len(R_vals)}] R={R:.3f} Å → E={E:.4f} eV")
    
    with open('results/h2_scan.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['R_A', 'E_eV'])
        writer.writeheader()
        writer.writerows(results)
    
    # Find minimum
    E_arr = np.array([r['E_eV'] for r in results])
    idx_min = np.argmin(E_arr)
    R_eq = R_vals[idx_min]
    
    # Fit quadratic around minimum (±3 points)
    i_fit = slice(max(0, idx_min-3), min(len(R_vals), idx_min+4))
    coeffs = np.polyfit(R_vals[i_fit], E_arr[i_fit], 2)
    R_eq_fit = -coeffs[1]/(2*coeffs[0])
    k_approx = 2*coeffs[0]  # eV/Å²
    
    print(f"\n✅ R_eq = {R_eq_fit:.3f} Å, k ≈ {k_approx:.2f} eV/Å²")
    
    # Plot
    plt.figure(figsize=(10,6))
    plt.plot(R_vals, E_arr, 'o-', linewidth=2, markersize=8, label='DFT (PBE)')
    plt.axvline(R_eq_fit, color='red', linestyle='--', label=f'R_eq={R_eq_fit:.3f} Å')
    plt.xlabel('H-H Distance (Å)', fontweight='bold', fontsize=12)
    plt.ylabel('Energy (eV)', fontweight='bold', fontsize=12)
    plt.title('H₂ Potential Energy Curve', fontweight='bold', fontsize=13)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('plots/h2_E_vs_R.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Saved: plots/h2_E_vs_R.png")
    
    return {'R_eq': R_eq_fit, 'k': k_approx}

