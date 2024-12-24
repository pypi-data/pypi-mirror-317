# AlloySustainability/computations.py
import pandas as pd
import os
import requests
from io import StringIO

GITHUB_RAW_URL = "https://raw.githubusercontent.com/sgorsse/AlloySustainability/1e4442e70765e9b9096743aa66479a182d56d41b/data/gen_18element_imputed_v202412.csv"

def load_element_indicators():
    response = requests.get(GITHUB_RAW_URL)
    response.raise_for_status()
    csv_data = StringIO(response.text)
    element_indicators = pd.read_csv(csv_data, sep=',')
    element_indicators = element_indicators.set_index('elements')
    return element_indicators

def load_embedded_data(file_name):
    data_path = os.path.join(os.path.dirname(__file__), "data", file_name)
    return pd.read_csv(data_path, sep=';')

def load_RTHEAs_vs_Fe_df():
    return load_embedded_data("gen_RTHEAs_vs_Fe_df.csv")

def load_HTHEAs_vs_Ni_df():
    return load_embedded_data("gen_HTHEAs_vs_Ni_df.csv")

def compute_impacts(composition_mass, element_indicators):
    if len(composition_mass) != 18:
        raise ValueError("The mass composition must include 18 elements.")

    element_names = ['Al', 'Co', 'Cr', 'Cu', 'Fe', 'Hf',
                     'Mn', 'Mo', 'Nb', 'Ni', 'Re', 'Ru', 
                     'Si', 'Ta', 'Ti', 'V', 'W', 'Zr']
    
    alloy_compo_mass = pd.DataFrame([composition_mass], columns=element_names)

    new_alloy_impacts = pd.DataFrame()
    new_alloy_impacts['Mass price (USD/kg)'] = alloy_compo_mass.dot(element_indicators['Raw material price (USD/kg)'])
    result = (1 - alloy_compo_mass * element_indicators[['Supply risk']].T.values)
    new_alloy_impacts['Supply risk'] = 1 - result.prod(axis=1)
    new_alloy_impacts['Normalized vulnerability to supply restriction'] = alloy_compo_mass.dot(element_indicators['Normalized vulnerability to supply restriction'])
    new_alloy_impacts['Embodied energy (MJ/kg)'] = alloy_compo_mass.dot(element_indicators['Embodied energy (MJ/kg)'])
    new_alloy_impacts['Water usage (l/kg)'] = alloy_compo_mass.dot(element_indicators['Water usage (l/kg)'])
    new_alloy_impacts['Rock to metal ratio (kg/kg)'] = alloy_compo_mass.dot(element_indicators['Rock to metal ratio (kg/kg)'])
    new_alloy_impacts['Human health damage'] = alloy_compo_mass.dot(element_indicators['Human health damage'])
    new_alloy_impacts['Human rights pressure'] = alloy_compo_mass.dot(element_indicators['Human rights pressure'])
    new_alloy_impacts['Labor rights pressure'] = alloy_compo_mass.dot(element_indicators['Labor rights pressure'])

    return new_alloy_impacts
