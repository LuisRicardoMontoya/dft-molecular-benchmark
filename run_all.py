#!/usr/bin/env python3
"""
DFT Molecular Benchmark Pipeline
ASE + GPAW | Reproducible Workflow

Generates:
- Molecular properties (SCF, optimization)
- H2 bond scan
- Electronic properties (HOMO/LUMO/gap)
- Charges and dipoles
- DOS plots
- Full PDF report
"""

import sys
import os
import json
import time
from datetime import datetime
import platform
import psutil

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ============================================================================
# METADATA COLLECTION
# ============================================================================

def collect_metadata():
    """Collect system and software metadata"""
    
    import ase
    import gpaw
    import numpy as np
    
    metadata = {
        'timestamp_start': datetime.now().isoformat(),
        'python_version': sys.version,
        'ase_version': ase.__version__,
        'gpaw_version': gpaw.__version__,
        'numpy_version': np.__version__,
        'platform': {
            'system': platform.system(),
            'release': platform.release(),
            'machine': platform.machine(),
            'processor': platform.processor()
        },
        'hardware': {
            'cpu_count': psutil.cpu_count(logical=False),
            'cpu_count_logical': psutil.cpu_count(logical=True),
            'ram_gb': round(psutil.virtual_memory().total / (1024**3), 2),
            'gpu': 'NVIDIA A10 (24GB)' if os.path.exists('/dev/nvidia0') else 'None detected'
        },
        'dft_parameters': {
            'xc_functional': 'PBE',
            'mode': 'fd',  # finite difference
            'energy_convergence': 1e-5,  # eV
            'force_convergence': 0.02,  # eV/Å
            'vacuum': 7.0,  # Å
            'grid_spacing': 0.18  # Å
        },
        'molecules': ['H2', 'CO', 'H2O', 'NH3'],
        'h2_scan': {
            'R_min': 0.5,  # Å
            'R_max': 2.5,  # Å
            'n_points': 15
        }
    }
    
    return metadata

# ============================================================================
# MAIN PIPELINE
# ============================================================================

def main():
    print("="*80)
    print("🧪 DFT MOLECULAR BENCHMARK PIPELINE")
    print("   ASE + GPAW | PBE Functional")
    print("="*80)
    
    start_time = time.time()
    
    # Collect metadata
    print("\n📋 Collecting metadata...")
    metadata = collect_metadata()
    
    print(f"   Python: {metadata['python_version'].split()[0]}")
    print(f"   ASE: {metadata['ase_version']}")
    print(f"   GPAW: {metadata['gpaw_version']}")
    print(f"   CPUs: {metadata['hardware']['cpu_count']} physical, {metadata['hardware']['cpu_count_logical']} logical")
    print(f"   RAM: {metadata['hardware']['ram_gb']} GB")
    print(f"   GPU: {metadata['hardware']['gpu']}")
    
    # Save initial metadata
    with open('results/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n✅ Metadata saved: results/metadata.json")
    
    # Import calculation modules
    print("\n📦 Loading calculation modules...")
    from modules import molecular_calcs, h2_scan, electronic_props, eda, report_gen
    
    # Step 1: Molecular calculations (SCF + optimization)
    print("\n" + "="*80)
    print("STEP 1: MOLECULAR CALCULATIONS (H2, CO, H2O, NH3)")
    print("="*80)
    molecular_results = molecular_calcs.run_all_molecules(metadata)
    
    # Step 2: H2 bond scan
    print("\n" + "="*80)
    print("STEP 2: H2 BOND SCAN (0.5 - 2.5 Å, 15 points)")
    print("="*80)
    h2_scan_results = h2_scan.run_h2_scan(metadata)
    
    # Step 3: Electronic properties (charges, HOMO/LUMO, DOS)
    print("\n" + "="*80)
    print("STEP 3: ELECTRONIC PROPERTIES")
    print("="*80)
    electronic_results = electronic_props.extract_all_properties(molecular_results, metadata)
    
    # Step 4: EDA + plots
    print("\n" + "="*80)
    print("STEP 4: EXPLORATORY DATA ANALYSIS")
    print("="*80)
    eda.generate_all_plots()
    
    # Step 5: PDF report
    print("\n" + "="*80)
    print("STEP 5: GENERATING PDF REPORT")
    print("="*80)
    report_gen.generate_pdf_report(metadata)
    
    # Final metadata
    elapsed = time.time() - start_time
    metadata['timestamp_end'] = datetime.now().isoformat()
    metadata['total_runtime_seconds'] = elapsed
    
    with open('results/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "="*80)
    print("✅ PIPELINE COMPLETED SUCCESSFULLY")
    print("="*80)
    print(f"\n⏱️  Total runtime: {elapsed/60:.1f} minutes")
    print(f"\n📁 Outputs:")
    print(f"   - results/*.csv (molecular_summary, h2_scan, charges, electronic_properties)")
    print(f"   - plots/*.png ({len([f for f in os.listdir('plots') if f.endswith('.png')])} figures)")
    print(f"   - pdf/dft_molecular_report.pdf")
    print(f"   - results/metadata.json")
    
    # Create manifest
    manifest = {
        'generated_files': {
            'csvs': [f for f in os.listdir('results') if f.endswith('.csv')],
            'plots': [f for f in os.listdir('plots') if f.endswith('.png')],
            'pdf': 'pdf/dft_molecular_report.pdf',
            'metadata': 'results/metadata.json'
        },
        'summary': {
            'molecules_calculated': len(metadata['molecules']),
            'h2_scan_points': metadata['h2_scan']['n_points'],
            'total_runtime_min': round(elapsed/60, 2),
            'status': 'SUCCESS'
        }
    }
    
    with open('reports/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n✅ Manifest saved: reports/manifest.json")

if __name__ == '__main__':
    main()

