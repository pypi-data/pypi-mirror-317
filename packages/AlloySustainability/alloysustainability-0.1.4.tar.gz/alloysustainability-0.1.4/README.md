# AlloySustainability

**AlloySustainability** is a Python package designed to compute and visualize the sustainability impacts of alloys based on their elemental composition. It retrieves key indicators from external data sources (including a file automatically downloaded from GitHub) and produces comprehensive metrics and visualizations.

## Features

- **Compute Indicators**: Given the mass fractions of 18 elements composing an alloy, compute a range of sustainability indicators (e.g., mass price, supply risk, embodied energy, water usage).
- **Embedded Data**: The package includes two CSV files (`gen_RTHEAs_vs_Fe_df.csv`, `gen_HTHEAs_vs_Ni_df.csv`) embedded within the package, providing baseline reference data for comparison.
- **Automatic Data Retrieval**: A third CSV file (`gen_18element_imputed_v202412.csv`) is automatically downloaded from GitHub, ensuring that you always have the latest data.
- **Visualization**: Easily generate comparative plots (e.g., violin plots) to compare the new alloy’s metrics against reference classes such as FCC HEAs, BCC HEAs, Steels, and Ni-based alloys.

## Installation

Install AlloySustainability directly from PyPI:

```
pip install AlloySustainability
```

## Usage

```
from AlloySustainability.computations import (
    load_element_indicators,
    load_RTHEAs_vs_Fe_df,
    load_HTHEAs_vs_Ni_df,
    compute_impacts
)
from AlloySustainability.visualization import plot_alloy_comparison
import matplotlib.pyplot as plt

# Load data
element_indicators = load_element_indicators()
RTHEAs_Fe_df = load_RTHEAs_vs_Fe_df()
HTHEAs_Ni_df = load_HTHEAs_vs_Ni_df()

# Define the alloy composition (mass fractions of 18 elements)
# Make sure the fractions sum up to 1.0
composition_mass = [0, 0.2, 0.2, 0, 0, 0, 0.2, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0.2]

# Compute the sustainability impacts
new_alloy_impacts = compute_impacts(composition_mass, element_indicators)

# Visualize the alloy impacts compared to reference classes
fig = plot_alloy_comparison(new_alloy_impacts, RTHEAs_Fe_df, HTHEAs_Ni_df)
plt.show()

```

## Requirements

- Python 3.6+
- numpy
- pandas
- matplotlib
- seaborn
- requests

## Further Reading

For more information on sustainability indicators in the context of high entropy alloys, please refer to:

Considering sustainability when searching for new high entropy alloys
S. Gorsse, T. Langlois, M. R. Barnett
Sustainable Materials and Technologies 40 (2024) e00938
https://doi.org/10.1016/j.susmat.2024.e00938
