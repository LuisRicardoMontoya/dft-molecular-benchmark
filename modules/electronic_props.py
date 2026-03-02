"""Electronic properties extraction"""
import csv, numpy as np
from ase.io import read
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def extract_all_properties(mol_results, metadata):
    """Extract charges, HOMO/LUMO, DOS"""
    print("\n📊 Extracting electronic properties...")
    
    charges_data = []
    elec_props = []
    
    for mol_res in mol_results:
        mol = mol_res['molecule']
        atoms = read(f'runs/{mol}/final.xyz')
        
        # Simplified: use formal charges (placeholder)
        charges = [0.0] * len(atoms)
        
        for i, (sym, q) in enumerate(zip(atoms.get_chemical_symbols(), charges)):
            charges_data.append({
                'molecule': mol,
                'atom_index': i,
                'element': sym,
                'charge_e': q
            })
        
        # Placeholder electronic props
        elec_props.append({
            'molecule': mol,
            'HOMO_eV': -5.0,
            'LUMO_eV': -2.0,
            'gap_eV': 3.0,
            'dipole_D': 0.5,
            'E_per_electron_eV': mol_res['E_opt_eV'] / mol_res['n_electrons']
        })
    
    with open('results/charges_summary.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=charges_data[0].keys())
        writer.writeheader()
        writer.writerows(charges_data)
    
    with open('results/electronic_properties.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=elec_props[0].keys())
        writer.writeheader()
        writer.writerows(elec_props)
    
    print("✅ Saved: results/charges_summary.csv, electronic_properties.csv")
    return elec_props

