"""Molecular DFT calculations"""
import os, csv, time
import numpy as np
from ase import Atoms
from ase.optimize import BFGS
from ase.io import write
from gpaw import GPAW

def get_molecule(name):
    """Create molecule geometry"""
    if name == 'H2':
        return Atoms('H2', positions=[[0,0,0], [0.74,0,0]])
    elif name == 'CO':
        return Atoms('CO', positions=[[0,0,0], [1.13,0,0]])
    elif name == 'H2O':
        return Atoms('OH2', positions=[[0,0,0], [0.96,0,0], [0.24,0.93,0]])
    elif name == 'NH3':
        return Atoms('NH3', positions=[[0,0,0], [1.01,0,0], [-0.33,0.95,0], [-0.33,-0.48,0.82]])

def run_molecule(name, params):
    """SCF + optimization for one molecule"""
    print(f"\n{'='*60}\n🔬 {name}\n{'='*60}")
    
    os.makedirs(f'runs/{name}', exist_ok=True)
    
    atoms = get_molecule(name)
    atoms.center(vacuum=params['vacuum'])
    atoms.set_pbc(True)
    
    calc = GPAW(mode='fd', xc='PBE', h=params['grid_spacing'], 
                txt=f'runs/{name}/scf.txt', convergence={'energy': params['energy_convergence']})
    atoms.calc = calc
    
    t0 = time.time()
    E_scf = atoms.get_potential_energy()
    t_scf = time.time() - t0
    
    print(f"✅ SCF: {E_scf:.4f} eV ({t_scf:.1f}s)")
    
    # Optimization
    t0 = time.time()
    opt = BFGS(atoms, trajectory=f'runs/{name}/opt.traj', logfile=f'runs/{name}/opt.log')
    opt.run(fmax=params['force_convergence'])
    E_opt = atoms.get_potential_energy()
    t_opt = time.time() - t0
    
    write(f'runs/{name}/final.xyz', atoms)
    
    fmax = np.max(np.abs(atoms.get_forces()))
    
    print(f"✅ Opt: {E_opt:.4f} eV ({t_opt:.1f}s, fmax={fmax:.4f})")
    
    # Extract geometry
    pos = atoms.get_positions()
    bonds, angles = [], []
    
    if name == 'H2':
        bonds = [np.linalg.norm(pos[1]-pos[0])]
    elif name == 'CO':
        bonds = [np.linalg.norm(pos[1]-pos[0])]
    elif name == 'H2O':
        oh1, oh2 = np.linalg.norm(pos[1]-pos[0]), np.linalg.norm(pos[2]-pos[0])
        bonds = [oh1, oh2]
        v1, v2 = pos[1]-pos[0], pos[2]-pos[0]
        angles = [np.degrees(np.arccos(np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))))]
    elif name == 'NH3':
        bonds = [np.linalg.norm(pos[i]-pos[0]) for i in [1,2,3]]
        v1, v2 = pos[1]-pos[0], pos[2]-pos[0]
        angles = [np.degrees(np.arccos(np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))))]
    
    return {
        'molecule': name,
        'E_scf_eV': E_scf,
        'E_opt_eV': E_opt,
        'n_electrons': len(atoms)*2,  # approx
        'runtime_scf_s': t_scf,
        'runtime_opt_s': t_opt,
        'final_forces_max_eV_A': fmax,
        'bond_lengths_A': ','.join(f'{b:.3f}' for b in bonds),
        'angles_deg': ','.join(f'{a:.1f}' for a in angles) if angles else ''
    }

def run_all_molecules(metadata):
    results = []
    for mol in metadata['molecules']:
        try:
            res = run_molecule(mol, metadata['dft_parameters'])
            results.append(res)
        except Exception as e:
            print(f"❌ {mol} failed: {e}")
    
    with open('results/molecular_summary.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print("\n✅ Saved: results/molecular_summary.csv")
    return results

