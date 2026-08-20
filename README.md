# pI Charge Consensus

Multi-algorithm protein isoelectric point (pI) calculation, charge-vs-pH titration profiling, and ion exchange chromatography buffer optimization for peptides and proteins.

# Overview

`pi-charge-consensus` is a scientific bioinformatics tool designed to resolve discrepancies in theoretical isoelectric point ($\text{pI}$) and net charge calculations for proteins and peptides. The theoretical isoelectric point is the specific pH at which a protein carries zero net electrical charge ($\text{net charge} = 0$). Calculating accurate $\text{pI}$ values and charge profiles across pH gradients ($0\text{--}14$) is essential in protein biochemistry, structural biology, biopharmaceutical formulation, post-translational modification (PTM) analysis, and downstream purification techniques such as Isoelectric Focusing (IEF), 2D Gel Electrophoresis (2D-PAGE), Anion Exchange Chromatography (AEX), and Cation Exchange Chromatography (CEX).

Because different empirical $\text{p}K_a$ scales (e.g., Bjellqvist, IPC 1.0, IPC 2.0 ML, EMBOSS, and ProMoST) yield varying $\text{pI}$ estimates depending on their underlying experimental calibration sets and training datasets, relying on a single algorithm can lead to erroneous experimental conditions in protein purification and assay design. `pi-charge-consensus` computes parallel $\text{pI}$ estimations across five recognized $\text{p}K_a$ algorithms, reporting a consensus mean $\text{pI}$, minimum/maximum variance boundaries, standard deviation, net charge at physiological or target pH, molar extinction coefficients ($\varepsilon_{280}$), absorbance at 280 nm ($A_{280}$), and automated buffer recommendation for ion exchange chromatography.

Researchers can access the interactive web application at https://www.pepkio.com/tools/pi-charge-consensus or integrate the Python client library and CLI into automated bioinformatics pipelines.

# Features

* **Multi-Algorithm Consensus pI Engine**: Executes five pKa algorithms in parallel: Bjellqvist (ExPASy Compute pI/Mw), IPC 1.0 (Isoelectric Point Calculator), IPC 2.0 ML (Machine Learning-based pI model), EMBOSS, and ProMoST.
* **Consensus Statistics**: Calculates consensus mean pI, minimum pI, maximum pI, and standard deviation ($\sigma_{\text{pI}}$) to quantify algorithmic confidence and boundary uncertainty.
* **Charge vs. pH Titration Curve**: Generates continuous net charge values across the pH spectrum ($0.0\text{--}14.0$ at $0.1$ pH increments) to model ionization state changes.
* **Ion Exchange Chromatography (IEX) Buffer Advisor**: Automates buffer pH selection and exchanger type recommendations (Anion Exchanger vs. Cation Exchanger) based on calculated pI thresholds.
* **Post-Translational Modification (PTM) Toggles**: Evaluates charge shifts caused by Ser/Thr phosphorylation, N-linked glycosylation, disulfide bond formation (Cys oxidation state), N-terminal acetylation, and C-terminal amidation.
* **Physicochemical Properties**: Computes exact molecular weight ($\text{Da}$ / $\text{kDa}$), reduced and oxidized molar extinction coefficients ($\varepsilon_{280}$ in $\text{M}^{-1}\text{cm}^{-1}$), and $A_{280}$ absorbance values ($1\text{ mg/mL}$).
* **High-Throughput Batch FASTA Mode**: Processes multi-FASTA inputs (up to 200 protein sequences per request) with output metrics structured for virtual 2D-PAGE plots and proteomic profiling.
* **Dual Execution Interfaces**: Full programmatic control via a Python SDK and Command-Line Interface (CLI), backed by a web interface.

# Common Use Cases

* **Ion Exchange Chromatography (IEX) Optimization**: Determine whether to use strong/weak anion exchangers (e.g., Q Sepharose, DEAE) or cation exchangers (e.g., SP Sepharose, CM Sepharose) by identifying the pH ranges where the target protein holds a stable net positive or net negative charge.
* **Recombinant Protein Expression & Purification**: Predict protein solubility and aggregation risks by evaluating proximity to the isoelectric point during cell lysis, salt precipitation, and buffer exchange steps.
* **Post-Translational Modification (PTM) Profiling**: Calculate charge and pI shifts induced by enzymatic phosphorylation, N-terminal blocking, or C-terminal modifications in modified peptides and enzymes.
* **Proteomics & 2D Gel Electrophoresis (2D-PAGE)**: Predict first-dimension isoelectric focusing migration patterns and second-dimension SDS-PAGE separation boundaries for batch FASTA datasets.
* **Biopharmaceutical & Antibody Formulation**: Assess stability windows and colloidal solubility of monoclonal antibodies (mAbs) and therapeutic proteins in formulation buffers across target pH regimes (e.g., pH 5.5–7.4).

# Why This Tool Exists

Calculating protein isoelectric points using single-scale algorithms or simplified spreadsheet formulas often leads to experimental failures in protein purification:

1. **Algorithm Discrepancies**: Different $\text{p}K_a$ lookup tables produce $\text{pI}$ variations exceeding $0.5\text{--}1.0$ pH units for the same amino acid sequence. For instance, basic or acidic proteins frequently exhibit significant divergence between classic Bjellqvist pKa sets and modern machine-learning models like IPC 2.0.
2. **Ignored Modifications**: Basic calculators assume static, unmodified amino acid side chains, failing to account for N-terminal acetylation, C-terminal amidation, or phosphorylation, which dramatically alter net charge and pI.
3. **Manual Spectrophotometry Calculations**: Calculating molar extinction coefficients ($\varepsilon_{280}$) and converting absorbance ($A_{280}$) manually is prone to human error when accounting for cystine disulfide bridges versus free cysteine thiols.
4. **Lack of Automated Buffer Selection**: Chromatographic protocols require selecting binding buffer pH at least $1.0\text{--}1.5$ units away from the protein pI. Manual calculations require plotting titration curves by hand.

`pi-charge-consensus` resolves these limitations by synthesizing multiple empirical models into a single, automated, reproducible workflow.

# Installation

Install the `pepkio-pi-charge-consensus` Python package from PyPI (https://pypi.org/project/pepkio-pi-charge-consensus/) using `pip` or `uv`:

```bash
pip install pepkio-pi-charge-consensus
```

Or using `uv`:

```bash
uv add pepkio-pi-charge-consensus
```

### Environment Setup

Set your Pepkio API key as an environment variable:

```bash
export PEPKIO_API_KEY="your_api_key_here"
```

# Quick Start

The package can be used as a Python library or via the command-line interface (CLI).

### Python Library Usage

```python
import os
from pepkio_pi_charge_consensus import PepkioClient

# Initialize client (uses PEPKIO_API_KEY environment variable)
client = PepkioClient()

# Single protein sequence calculation
sequence = "KVFERCELARTLKRLGMDGYRGISLANWMCLAKWESGYNTRATNYNAGDRSTDYGIFQINSRYWCNDGKTPGAVNACHLSCSALLQDNIADAVACAKRVVRDPQGIRAWVAWRNRCQNRDVRQYVQGCGV"

result = client.run({
    "tab": "single",
    "sequence": sequence,
    "sequence_name": "Hen Egg White Lysozyme",
    "algorithms": ["bjellqvist", "emboss", "ipc_1", "ipc_2", "promost"],
    "target_ph": 7.4,
    "disulfide_bonds": True
})

protein_data = result.result["sequences"][0]

print(f"Protein: {protein_data.get('name', 'Lysozyme')}")
print(f"Consensus pI: {protein_data['consensus_pi']:.2f}")
print(f"pI Range: {protein_data['pi_min']:.2f} - {protein_data['pi_max']:.2f} (StdDev: {protein_data['pi_std_dev']:.2f})")
print(f"Molecular Weight: {protein_data['mw_kda']:.2f} kDa")
print(f"Net Charge at pH 7.4: {protein_data['charge_at_target_ph']:+.2f}")
print(f"Extinction Coefficient (280 nm): {protein_data['epsilon_280']} M^-1 cm^-1")
print(f"IEX Exchanger Recommendation: {protein_data['buffer']['exchanger']}")
print(f"IEX Buffer Window: pH {protein_data['buffer']['ph_min']:.2f} - {protein_data['buffer']['ph_max']:.2f}")
```

### Batch FASTA Processing

```python
fasta_data = """>sp|P00698|LYSC_CHICK Lysozyme C
KVFERCELARTLKRLGMDGYRGISLANWMCLAKWESGYNTRATNYNAGDRSTDYGIFQINSRYWCNDGKTPGAVNACHLSCSALLQDNIADAVACAKRVVRDPQGIRAWVAWRNRCQNRDVRQYVQGCGV
>sp|P01308|INS_HUMAN Insulin
GIVEQCCTSICSLYQLENYCNFVNQHLCGSHLVEALYLVCGERGFFYTPKT
"""

result = client.run({
    "tab": "batch",
    "fasta_text": fasta_data,
    "target_ph": 7.0
})

for seq in result.result["sequences"]:
    print(f"Header: {seq['header']}")
    print(f"  Length: {seq['length']} aa | Mw: {seq['mw_kda']:.2f} kDa | Consensus pI: {seq['consensus_pi']:.2f}")
```

### Command-Line Interface (CLI)

List available preset examples:

```bash
pepkio-pi-charge-consensus manifest --examples
```

Run a single sequence calculation via JSON input:

```bash
pepkio-pi-charge-consensus run --input-json '{
  "tab": "single",
  "sequence": "KVFERCELARTLKRLGMDGYRGISLANWMCLAKWESGYNTRATNYNAGDRSTDYGIFQINSRYWCNDGKTPGAVNACHLSCSALLQDNIADAVACAKRVVRDPQGIRAWVAWRNRCQNRDVRQYVQGCGV",
  "target_ph": 7.4
}'
```

Run a preset manifest example:

```bash
pepkio-pi-charge-consensus run --example lysozyme_single
```

# Example Output

Below is an abbreviated example of the JSON response returned by `pi-charge-consensus` for Hen Egg White Lysozyme ($130$ amino acids):

```json
{
  "tab": "single",
  "sequences": [
    {
      "sequence": "KVFERCELARTLKRLGMDGYRGISLANWMCLAKWESGYNTRATNYNAGDRSTDYGIFQINSRYWCNDGKTPGAVNACHLSCSALLQDNIADAVACAKRVVRDPQGIRAWVAWRNRCQNRDVRQYVQGCGV",
      "length": 130,
      "algorithms": [
        { "algorithm": "bjellqvist", "label": "Bjellqvist", "pi": 9.28 },
        { "algorithm": "ipc_1", "label": "IPC 1.0", "pi": 8.37 },
        { "algorithm": "ipc_2", "label": "IPC 2.0 ML", "pi": 8.41 },
        { "algorithm": "emboss", "label": "EMBOSS", "pi": 9.14 },
        { "algorithm": "promost", "label": "ProMoST", "pi": 8.79 }
      ],
      "consensus_pi": 8.8,
      "pi_min": 8.37,
      "pi_max": 9.28,
      "pi_std_dev": 0.41,
      "mw_da": 14700.53,
      "mw_kda": 14.7,
      "epsilon_280": 36440,
      "a280_01pct": 2.4788,
      "charge_at_target_ph": 7.377,
      "buffer": {
        "ph_min": 8.3,
        "ph_max": 9.3,
        "exchanger": "cation",
        "note": "Bind at pH <= 8.30 using cation exchanger (CM/SP), or pH >= 9.30 using anion exchanger (DEAE/Q)"
      }
    }
  ]
}
```

# Scientific Background

### Isoelectric Point ($\text{pI}$) & Henderson-Hasselbalch Equation

The net charge of a protein as a function of environmental $\text{pH}$ is determined by the ionization state of its N-terminal amino group, C-terminal carboxyl group, and seven ionizable amino acid side chains (Asp, Glu, His, Cys, Tyr, Lys, Arg).

The positive charge contribution of basic groups (N-terminus, Lys, Arg, His) at a given $\text{pH}$ is governed by:

$$q_i^+ = \frac{1}{1 + 10^{(\text{pH} - \text{p}K_{a,i})}}$$

The negative charge contribution of acidic groups (C-terminus, Asp, Glu, Cys, Tyr) is governed by:

$$q_j^- = \frac{-1}{1 + 10^{(\text{p}K_{a,j} - \text{pH})}}$$

The total net charge $Z(\text{pH})$ is the sum of all individual partial charges:

$$Z(\text{pH}) = \sum_{i} q_i^+ + \sum_{j} q_j^-$$

The isoelectric point ($\text{pI}$) is mathematically defined as the root of the charge function where net charge equals zero:

$$Z(\text{pI}) = 0$$

`pi-charge-consensus` solves for $\text{pI}$ using a bisection algorithm across the $\text{pH}$ range $0.0\text{--}14.0$ until $|Z(\text{pH})| < 0.0001$.

### Empirical $\text{p}K_a$ Scales & Algorithms

Different algorithms utilize distinct experimental or calculated $\text{p}K_a$ datasets:

| Algorithm / Scale | Reference | Primary Application & Notes |
| :--- | :--- | :--- |
| **Bjellqvist** | Bjellqvist et al. (1993/1994) | ExPASy Compute pI/Mw standard; calibrated using 2D-PAGE immobilized pH gradients. |
| **IPC 1.0** | Kozlowski (2016) | Derived from extensive peptide datasets; optimized for high predictive accuracy across diverse proteins. |
| **IPC 2.0 ML** | Kozlowski (2021) | Support Vector Regression (SVR) machine learning model trained on experimental pI datasets. |
| **EMBOSS** | Rice et al. (2000) | Classic European Molecular Biology Open Software Suite pKa lookup table. |
| **ProMoST** | Halligan et al. (2004) | Calculates pI and Mw shifts specifically modeling post-translational modifications (PTMs). |

### Molar Extinction Coefficient ($\varepsilon_{280}$)

Protein concentration determination at $280\text{ nm}$ relies on the molar extinction coefficient ($\varepsilon_{280}$), calculated according to Pace et al. (1995):

$$\varepsilon_{280}\ (\text{M}^{-1}\text{cm}^{-1}) = (\text{Count}_{\text{Trp}} \times 5500) + (\text{Count}_{\text{Tyr}} \times 1490) + (\text{Count}_{\text{Cys-Cys}} \times 125)$$

Where $\text{Count}_{\text{Cys-Cys}}$ represents the number of cystine disulfide bonds. For fully reduced proteins, cysteine contributions are zero.

Absorbance of a $0.1\%$ ($1\text{ mg/mL}$) solution is calculated as:

$$A_{280}^{0.1\%} = \frac{\varepsilon_{280}}{\text{Molecular Weight (Da)}}$$

### Ion Exchange Chromatography (IEX) Selection Rules

* **Cation Exchange (CEX)**: When $\text{pH} < \text{pI} - 0.5$, the protein carries a net positive charge ($Z > 0$) and binds positively charged resins (e.g., Carboxymethyl [CM], Sulfopropyl [SP]).
* **Anion Exchange (AEX)**: When $\text{pH} > \text{pI} + 0.5$, the protein carries a net negative charge ($Z < 0$) and binds negatively charged resins (e.g., Diethylaminoethyl [DEAE], Quaternary Ammonium [Q]).

# Frequently Asked Questions

### What is an isoelectric point (pI)?
The isoelectric point ($\text{pI}$) is the pH at which a protein or peptide carries no net electrical charge ($Z = 0$). At this pH, the number of positively charged functional groups equals the number of negatively charged functional groups, rendering the molecule electrophoretically immobile in an unbuffered electric field.

### How does pi-charge-consensus calculate the consensus pI?
`pi-charge-consensus` computes individual $\text{pI}$ values using five distinct empirical $\text{p}K_a$ scales (Bjellqvist, IPC 1.0, IPC 2.0 ML, EMBOSS, and ProMoST). The consensus $\text{pI}$ is reported as the arithmetic mean of these calculations, accompanied by the minimum value, maximum value, and standard deviation to reflect model variance.

### Why do different pI calculators give different results for the same protein?
Different calculators employ different set values for amino acid $\text{p}K_a$ constants. $\text{p}K_a$ values are influenced by local microenvironments, dielectric constants, neighbor residue effects, and temperature. Algorithms calibrated on small synthetic peptides (e.g., IPC 1.0) differ from those calibrated on 2D-gel electrophoresis of intact folded proteins (e.g., Bjellqvist).

### What is IPC 2.0 ML?
IPC 2.0 (Isoelectric Point Calculator 2.0) is a machine learning algorithm based on Support Vector Regression (SVR) trained on thousands of experimentally determined protein and peptide $\text{pI}$ measurements. It accounts for sequence-context effects beyond static residue-level $\text{p}K_a$ lookup tables.

### How does phosphorylation affect protein pI and net charge?
Phosphorylation adds a phosphate group ($\text{PO}_4^{3-}$) to serine, threonine, or tyrosine residues. Each phosphate group introduces up to two negative charges at physiological pH ($\text{p}K_{a1} \approx 1.2$, $\text{p}K_{a2} \approx 6.5$), causing a significant drop in net charge and shifting the protein's overall $\text{pI}$ toward lower (acidic) values.

### How does N-terminal acetylation alter pI?
N-terminal acetylation caps the $\alpha$-amino group ($\text{R-NH}_3^+$), converting it into a neutral amide ($\text{R-NH-CO-CH}_3$). This eliminates a positive charge at acidic and neutral pH, resulting in an overall decrease in the protein's net charge and acidic shift in $\text{pI}$.

### How does C-terminal amidation alter pI?
C-terminal amidation converts the terminal carboxyl group ($\text{R-COO}^-$) into a neutral amide ($\text{R-CONH}_2$). This eliminates a negative charge, increasing the net charge and shifting the $\text{pI}$ toward higher (basic) values.

### How does disulfide bond formation affect the extinction coefficient?
Free cysteine thiols ($\text{-SH}$) do not absorb significantly at $280\text{ nm}$. When two cysteine residues form a cystine disulfide bond ($\text{-S-S-}$), the pair contributes $125\text{ M}^{-1}\text{cm}^{-1}$ to the molar extinction coefficient ($\varepsilon_{280}$).

### How do I select an Ion Exchange (IEX) buffer using pI?
To ensure strong binding in ion exchange chromatography, select a buffer pH at least $1\text{--}1.5$ units away from the protein's $\text{pI}$. If the buffer pH is below the $\text{pI}$, use a cation exchange column (e.g., SP Sepharose). If the buffer pH is above the $\text{pI}$, use an anion exchange column (e.g., Q Sepharose).

### What is physiological net charge at pH 7.4?
Physiological net charge is the net charge $Z$ calculated at $\text{pH } 7.4$. At this pH, glutamate and aspartate side chains are fully deprotonated (negative), lysine and arginine side chains are fully protonated (positive), and histidine side chains are partially protonated ($\sim 10\%$).

### Can I run pi-charge-consensus on batch FASTA files?
Yes. The tool supports multi-FASTA input containing up to 200 protein sequences in a single request. It parses headers and outputs sequence lengths, molecular weights, consensus $\text{pI}$ values, and extinction coefficients for high-throughput screening.

### What is the maximum sequence length supported?
The tool processes standard protein sequences of arbitrary length up to standard single-request memory limits ($512\text{ KB}$ input size), making it suitable for small peptides as well as large multi-domain proteins.

### Does the tool account for non-canonical amino acids?
Standard execution models canonical 20 amino acids alongside defined post-translational modification toggles (phosphorylation, acetylation, amidation, disulfide bonding, and N-linked glycosylation flags).

### How is protein absorbance at 280 nm ($A_{280}$) calculated?
Absorbance for a $0.1\%$ ($1\text{ mg/mL}$) protein solution ($A_{280}^{0.1\%}$) is derived by dividing the calculated molar extinction coefficient ($\varepsilon_{280}$) by the molecular weight in Daltons ($\text{Da}$).

### Why is consensus pI superior to single-algorithm calculation?
Using a consensus mean and standard deviation provides an empirical confidence interval, preventing experimental failure caused by single-scale predictive bias when designing ion exchange chromatography buffers or isoelectric focusing gels.

# Web Application

The hosted version of `pi-charge-consensus` is available at https://www.pepkio.com/tools/pi-charge-consensus.

The web version provides an interactive interface, shareable links, protocol generation, printable worksheets, and visualization tools.

Key web application capabilities include:

* **Interactive Titration Curves**: Dynamic plot rendering of charge-vs-pH curves ($0\text{--}14$) with hover inspection across target pH values.
* **Virtual 2D-PAGE Scatter Plots**: Interactive 2D visualization plotting consensus pI vs. Molecular Weight ($\text{kDa}$) for batch FASTA files.
* **Shareable Result Permalinks**: Persistent URLs allowing collaborators to view identical calculation outputs and parameters.
* **Downloadable Data Formats**: Export options for CSV, JSON, and printable laboratory summaries.
* **Amino Acid Composition Breakdown**: Visual pie charts and tables breaking down acidic, basic, hydrophobic, and neutral amino acid percentages.

Access the full web suite at https://www.pepkio.com/tools/pi-charge-consensus for interactive biochemical calculations.

# Related Resources

* GitHub Repository: https://github.com/pepkio/pepkio-pi-charge-consensus
* PyPI Package: https://pypi.org/project/pepkio-pi-charge-consensus/
* Web Application: https://www.pepkio.com/tools/pi-charge-consensus

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

Scientific capabilities include:

* RNA-seq analysis
* Single-cell RNA-seq analysis
* Spatial transcriptomics analysis
* Functional enrichment analysis
* Custom bioinformatics workflows

Website:
https://www.pepkio.com/

# Citation

If you use `pi-charge-consensus` or its underlying consensus algorithms in your research, please cite the software package and relevant pKa scale literature:

```bibtex
@software{pepkio_pi_charge_consensus_2026,
  author = {Pepkio Contributors},
  title = {pi-charge-consensus: Multi-algorithm protein isoelectric point and net charge consensus calculator},
  url = {https://github.com/pepkio/pepkio-pi-charge-consensus},
  year = {2026}
}

@article{kozlowski2021ipc,
  author = {Kozlowski, Lukasz P.},
  title = {IPC 2.0: prediction of isoelectric point and pKa values show that protein pI interval is broader than previously thought},
  journal = {Nucleic Acids Research},
  volume = {49},
  number = {W1},
  pages = {W285--W292},
  year = {2026},
  doi = {10.1093/nar/gkab295}
}

@article{bjellqvist1993isoelectric,
  author = {Bjellqvist, Bengt and Hughes, G. J. and Pasquali, C. and Paquet, N. and Ravier, F. and Sanchez, J. C. and Frutiger, S. and Hochstrasser, D.},
  title = {The focusing positions of polypeptides in immobilized pH gradients can be predicted from their amino acid sequences},
  journal = {Electrophoresis},
  volume = {14},
  number = {1},
  pages = {1023--1031},
  year = {1993},
  doi = {10.1002/elps.11501401163}
}
```

# License

This project is licensed under the MIT License - see the LICENSE file for details.

# Keywords

isoelectric point calculator
protein pi calculator
peptide charge calculator
pi charge consensus
protein net charge at ph
bjellqvist pka scale
ipc 2.0 isoelectric point
emboss pI calculation
promost pI calculator
molar extinction coefficient calculator
a280 extinction coefficient protein
ion exchange chromatography buffer selection
cation exchange chromatography ph selection
anion exchange chromatography ph selection
protein titration curve calculator
post translational modification pi shift
serine phosphorylation pi calculator
n-terminal acetylation net charge
c-terminal amidation charge shift
disulfide bond extinction coefficient
henderson hasselbalch protein charge
amino acid pka values
isoelectric focusing gel buffer
2d page virtual gel pi mw
expasy compute pi mw alternative
recombinant protein purification calculator
lysozyme isoelectric point
monoclonal antibody pi calculation
protein charge titration curve 0 to 14
fasta batch pi calculator
protein solubility ph prediction
protein pI standard deviation
consensus isoelectric point algorithm
protein charge state at ph 7.4
peptide pI calculator python
protein bioinformatics cli
pepkio pi charge consensus
protein charge calculator api
biochemical buffer recommendation tool
protein molecular weight calculator
extinction coefficient pace method
protein spectrophotometry calculator
theoretical isoelectric point algorithm
bioinformatics python sdk protein pi
pI range calculation protein
protein microenvironment pKa
acidic basic amino acid charge
isoelectric focusing protocol optimization
protein purification strategy ion exchange
batch fasta protein properties calculator
charge vs ph curve generator
protein charge calculation software
recombinant protein expression buffer optimization
biopharmaceutical mAb charge profiling
protein pKa lookup table comparison
bioinformatics REST API protein tools
