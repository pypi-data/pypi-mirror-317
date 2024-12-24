# AlloySustainability/visualization.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_alloy_comparison(new_alloy_impacts, RTHEAs_Fe_df, HTHEAs_Ni_df):

    indicators = [
        'Mass price (USD/kg)', 'Supply risk', 'Normalized vulnerability to supply restriction',
        'Embodied energy (MJ/kg)', 'Water usage (l/kg)', 'Rock to metal ratio (kg/kg)',
        'Human health damage', 'Human rights pressure', 'Labor rights pressure'
    ]

    fig, axes = plt.subplots(3, 3, figsize=(12, 12))
    fig.suptitle("Violin Plots of Indicators", fontsize=16, fontweight="bold")

    steels_df = RTHEAs_Fe_df[RTHEAs_Fe_df['Class'] == 'Steels']
    fcc_heas_df = RTHEAs_Fe_df[RTHEAs_Fe_df['Class'] == 'FCC HEAs']

    for idx, indicator in enumerate(indicators):
        row, col = divmod(idx, 3)
        ax = axes[row, col]
        
        data = pd.concat([
            pd.DataFrame({"Group": "Steels", "Value": steels_df[indicator]}),
            pd.DataFrame({"Group": "FCC HEAs", "Value": fcc_heas_df[indicator]}),
        ])

        sns.violinplot(x="Group", y="Value", data=data, ax=ax)
        new_alloy_value = float(new_alloy_impacts[indicator].iloc[0])
        ax.scatter(0.5, new_alloy_value, color="red", s=100, label="New Alloy")
        ax.set_title(f"{indicator} = {new_alloy_value:.2f}")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig

