# pepkio-pi-charge-consensus

A scientific Python package for computing consensus protein isoelectric points, net charge titration profiles across pH gradients, and optimal ion exchange chromatography buffer conditions using five empirical pKa algorithms.

# What It Does

`pepkio-pi-charge-consensus` evaluates theoretical protein and peptide isoelectric points (pI) and pH-dependent charge profiles. Because individual pKa algorithms (such as Bjellqvist or IPC 2.0) can diverge by up to 1.0 pH unit depending on their calibration datasets, this tool executes five established models in parallel (Bjellqvist, IPC 1.0, IPC 2.0 ML, EMBOSS, and ProMoST) to generate statistical consensus metrics. It calculates net charge across pH 0–14, predicts molecular weight and extinction coefficients ($A_{280}$), evaluates post-translational modifications (PTMs), and provides automated buffer pH and exchanger recommendations for ion exchange chromatography (IEX).

# Features

* **Multi-Algorithm Consensus Engine**: Simultaneously computes pI across Bjellqvist, IPC 1.0, IPC 2.0 ML, EMBOSS, and ProMoST.
* **Statistical Uncertainty Metrics**: Reports mean consensus pI, minimum/maximum range boundaries, and standard deviation ($\sigma_{\text{pI}}$).
* **Titration & Charge Profiling**: Generates continuous net charge values across the pH spectrum ($0.0\text{--}14.0$ at $0.1$ pH resolution).
* **IEX Buffer & Exchanger Selection**: Recommends anion (AEX) or cation (CEX) exchange resins and optimal binding buffer pH windows.
* **PTM Support**: Accounts for Ser/Thr phosphorylation, N-terminal acetylation, C-terminal amidation, and cystine disulfide bridges.
* **Physicochemical Properties**: Computes molecular weight (kDa), molar extinction coefficients ($\varepsilon_{280}$), and $A_{280}$ absorbance values.
* **Multi-FASTA Batch Processing**: Analyzes multi-sequence FASTA datasets for Virtual 2D-PAGE and proteomic screening.

# Installation

Install via `pip`:

```bash
pip install pepkio-pi-charge-consensus
```

Set your Pepkio API key as an environment variable:

```bash
export PEPKIO_API_KEY="your_api_key_here"
```

# Quick Example

```python
from pepkio_pi_charge_consensus import PepkioClient

# Initialize client and run consensus calculation for a target protein
with PepkioClient() as client:
    result = client.run({
        "tab": "single",
        "sequence": "KVFERCELARTLKRLGMDGYRGISLANWMCLAKWESGYNTRATNYNAGDRSTDYGIFQINSRYWCNDGKTPGAVNACHLSCSALLQDNIADAVACAKRVVRDPQGIRAWVAWRNRCQNRDVRQYVQGCGV",
        "sequence_name": "Lysozyme C",
        "target_ph": 7.4,
        "disulfide_bonds": True
    })

protein = result.result["sequences"][0]
print(f"Protein: {protein.get('name')}")
print(f"Consensus pI: {protein['consensus_pi']:.2f} (±{protein['pi_std_dev']:.2f})")
print(f"Net Charge at pH 7.4: {protein['charge_at_target_ph']:+.2f}")
print(f"Extinction Coefficient (ε280): {protein['epsilon_280']} M^-1 cm^-1")
print(f"IEX Exchanger: {protein['buffer']['exchanger']}")
print(f"Recommended Buffer pH: {protein['buffer']['ph_min']:.2f} - {protein['buffer']['ph_max']:.2f}")
```

# Typical Use Cases

* **Ion Exchange Chromatography (IEX) Optimization**: Select binding buffer pH ($1.0\text{--}1.5$ pH units away from pI) and determine whether to use anion (Q/DEAE) or cation (SP/CM) exchangers.
* **Recombinant Protein Purification**: Predict solubility windows and precipitation risks during cell lysis, salt fractionation, and buffer exchange.
* **Post-Translational Modification (PTM) Impact Analysis**: Quantify net charge and pI shifts resulting from phosphorylation, terminal blocking, or disulfide bond formation.
* **Proteomics & 2D-PAGE Separation**: Model first-dimension isoelectric focusing migration and second-dimension SDS-PAGE boundaries for multi-FASTA datasets.
* **Biopharmaceutical & Antibody Formulation**: Evaluate colloidal stability and net charge profiles of monoclonal antibodies (mAbs) and therapeutic proteins in formulation buffers.

# Scientific Background

The isoelectric point (pI) is the pH at which a protein carries zero net electrical charge. Theoretical pI values are calculated by iteratively solving Henderson-Hasselbalch equations across ionizable amino acid side chains and terminal groups. However, empirical pKa sets differ based on experimental calibration conditions (e.g., ExPASy Bjellqvist vs. IPC 2.0 machine learning models). Synthesizing multiple pKa scales into a consensus mean minimizes algorithm-specific bias and defines realistic pI variance boundaries for rational buffer design.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/pi-charge-consensus

Web-only features include interactive charge-vs-pH titration plots, custom pKa scale comparison overlays, visual IEX buffer selection diagrams, and exportable PDF/Excel summary worksheets.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-pi-charge-consensus

Web Application: https://www.pepkio.com/tools/pi-charge-consensus

Source code and issue tracker are hosted on [GitHub](https://github.com/pepkio/pepkio-pi-charge-consensus).

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro). See https://www.pepkio.com for additional tools and computational workflows.

# Keywords

* isoelectric point calculator
* protein pI calculation
* net charge titration
* pKa consensus algorithm
* Bjellqvist pKa scale
* IPC 2.0 ML pI prediction
* ion exchange chromatography buffer
* AEX CEX buffer advisor
* protein extinction coefficient
* A280 absorbance calculator
* post-translational modification charge shift
* protein phosphorylation pI
* disulfide bond charge calculation
* 2D-PAGE isoelectric focusing
* biopharmaceutical formulation pH
* peptide pI calculator
* protein molecular weight calculator
* ExPASy Compute pI Mw
* EMBOSS pKa scale
* ProMoST pKa algorithm
* protein solubility prediction
* mAb formulation stability
* multi-FASTA pI batch processing
* biophysics protein charge
* recombinant protein purification
* automated ion exchange chromatography buffer recommendation
* protein net charge calculation at target pH 7.4
* consensus pI standard deviation and variance boundary
* theoretical protein pI calculation using multiple pKa scales
* proteomic scale batch FASTA isoelectric point calculation
* net charge titration curve across pH spectrum 0 to 14
* PTM induced charge and pI shift calculation
* protein molar extinction coefficient ε280 calculation
* anion vs cation exchanger selection based on pI
* protein colloidal stability and solubility pH window
