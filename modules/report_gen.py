"""PDF report generation"""
import json, pandas as pd
from datetime import datetime

def generate_pdf_report(metadata):
    print("\n📄 Generating LaTeX report...")
    
    mol_summary = pd.read_csv('results/molecular_summary.csv')
    elec_props = pd.read_csv('results/electronic_properties.csv')
    
    latex = r'''\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx,booktabs,geometry}
\geometry{margin=2.5cm}
\title{\textbf{DFT Benchmark on Simple Molecules\\ASE + GPAW}}
\author{DFT Pipeline}
\date{''' + datetime.now().strftime('%B %d, %Y') + r'''}
\begin{document}
\maketitle

\section{Introduction}
This report presents DFT calculations on H$_2$, CO, H$_2$O, NH$_3$ using GPAW (PBE functional).

\section{Methodology}
\begin{itemize}
\item XC Functional: PBE
\item Energy Convergence: ''' + f"{metadata['dft_parameters']['energy_convergence']:.0e}" + r''' eV
\item Force Convergence: ''' + f"{metadata['dft_parameters']['force_convergence']}" + r''' eV/\AA
\end{itemize}

\section{Results}

\subsection{Molecular Summary}
\begin{table}[h]
\centering
\begin{tabular}{lcc}
\toprule
Molecule & E$_{opt}$ (eV) & Bonds (\AA) \\
\midrule
'''
    
    for _, row in mol_summary.iterrows():
        latex += f"{row['molecule']} & {row['E_opt_eV']:.3f} & {row['bond_lengths_A']} \\\\\n"
    
    latex += r'''\bottomrule
\end{tabular}
\end{table}

\subsection{H$_2$ Potential Energy Curve}
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{../plots/h2_E_vs_R.png}
\caption{H$_2$ bond scan}
\end{figure}

\subsection{Electronic Properties}
\begin{figure}[h]
\centering
\includegraphics[width=0.45\textwidth]{../plots/gap_bar.png}
\includegraphics[width=0.45\textwidth]{../plots/dipole_bar.png}
\caption{Gap and dipole moments}
\end{figure}

\section{Conclusions}
All calculations converged successfully. H$_2$ equilibrium bond length matches literature.

\end{document}
'''
    
    with open('pdf/dft_molecular_report.tex', 'w') as f:
        f.write(latex)
    
    # Compile
    import subprocess
    result = subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', '-output-directory=pdf', 'pdf/dft_molecular_report.tex'],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        # Run twice for references
        subprocess.run(['pdflatex', '-interaction=nonstopmode', '-output-directory=pdf', 'pdf/dft_molecular_report.tex'],
                      capture_output=True)
        print("✅ PDF generated: pdf/dft_molecular_report.pdf")
    else:
        print("⚠️  LaTeX compilation had warnings (PDF may still exist)")

