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

    categories = ["Economic viability", "Environmental impact", "Human well-being"]

    # Filtrer les groupes nécessaires à partir des DataFrames
    Steels_filtered = RTHEAs_Fe_df[RTHEAs_Fe_df['Class'] == 'Steels']
    FCC_HEAs_filtered = RTHEAs_Fe_df[RTHEAs_Fe_df['Class'] == 'FCC HEAs']
    Ni_filtered = HTHEAs_Ni_df[HTHEAs_Ni_df['Class'] == 'Ni superalloys']
    BCC_HEAs_filtered = HTHEAs_Ni_df[HTHEAs_Ni_df['Class'] == 'BCC HEAs']

    # Initialisation de la figure
    fig, axes = plt.subplots(3, 3, figsize=(12, 12))

    # Création des violons
    for idx, indicator in enumerate(indicators):
        row, col = divmod(idx, 3)
        ax = axes[row, col]

        # Préparation des données pour le violon
        data = pd.concat([
            pd.DataFrame({"Group": "Steels", "Dataset": "Steels", "Value": Steels_filtered[indicator]}),
            pd.DataFrame({"Group": "Ni-based", "Dataset": "Ni", "Value": Ni_filtered[indicator]}),
            pd.DataFrame({"Group": "FCC HEAs", "Dataset": "FCC HEAs", "Value": FCC_HEAs_filtered[indicator]}),
            pd.DataFrame({"Group": "BCC HEAs", "Dataset": "BCC HEAs", "Value": BCC_HEAs_filtered[indicator]})
        ])

        sns.violinplot(
            x="Group", y="Value", hue="Dataset", data=data, ax=ax, split=True,
            palette={"Steels": "#1f77b4", "Ni": "#ff7f0e", "FCC HEAs": "#2ca02c", "BCC HEAs": "#d62728"},
            inner=None, alpha=1, legend=False
        )

        # Ajuster l'échelle de y pour certains indicateurs
        if indicator == 'Mass price (USD/kg)':
            ax.set_yscale('log')
            ax.set_ylim(bottom=0.1)
        if indicator == 'Water usage (l/kg)':
            ax.set_yscale('log')
            ax.set_ylim(bottom=10)
        if indicator == 'Rock to metal ratio (kg/kg)':
            ax.set_yscale('log')
            ax.set_ylim(bottom=10)

        # Ajout des points pour la moyenne et la médiane
        mean_values = {
            "Steels": Steels_filtered[indicator].mean(),
            "Ni": Ni_filtered[indicator].mean(),
            "FCC HEAs": FCC_HEAs_filtered[indicator].mean(),
            "BCC HEAs": BCC_HEAs_filtered[indicator].mean()
        }
        median_values = {
            "Steels": Steels_filtered[indicator].median(),
            "Ni": Ni_filtered[indicator].median(),
            "FCC HEAs": FCC_HEAs_filtered[indicator].median(),
            "BCC HEAs": BCC_HEAs_filtered[indicator].median()
        }

        for group, color in zip(mean_values.keys(), ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]):
            ax.axhline(median_values[group], color=color, linestyle="-", label=f"Median {group}")

        # Ajout du point pour le nouvel alliage
        new_alloy_value = float(new_alloy_impacts[indicator].iloc[0])
        ax.scatter(1.5, new_alloy_value, color="black", s=100, label="New Alloy")

        # Titres et labels avec la valeur du nouvel alliage
        ax.set_title(f"{indicator} = {new_alloy_value:.2f}", fontsize=12, fontweight="bold")
        ax.set_ylabel("", fontsize=10)
        ax.set_xlabel("")
        if ax.get_yscale() != 'log':
            ax.set_ylim(bottom=0)  # Débuter l'axe y à 0 uniquement pour les axes non log
        ax.grid(True, linestyle="--", alpha=0.6)

    # Ajout des sous-titres pour chaque catégorie
    for row, category in enumerate(categories):
        axes[row, 0].annotate(category, xy=(-0.25, 0.5), xycoords="axes fraction", fontsize=14,
                              fontweight="bold", color="darkblue", rotation=90, ha="center", va="center")

    # Ajustement des marges et titre global
    fig.suptitle("Violin Plots of Indicators for HEAs and Conventional Alloys", fontsize=16, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig
