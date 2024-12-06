import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Configuration de la page Streamlit
st.set_page_config(page_title="Simulation des Réservoirs de Carbone", layout="wide")

# Charger les données d'émissions (fichier sans en-têtes)
data = pd.read_csv('emission.csv', header=None, sep=';')
data.columns = ['Year', 'Emissions']

# Extraire les colonnes
annees = data['Year']
emissions = data['Emissions']

# Ajouter des options pour les scénarios
st.sidebar.header("Choix du scénario à partir de 2020")
scenario = st.sidebar.selectbox(
    "Scénario d'émissions anthropiques",
    ["Business as usual", "-2%/an", "-5%/an"]
)

# Étendre les années pour couvrir 2020 à 2100
extended_years = list(range(2021, 2101))
annees_extended = list(annees) + extended_years
new_emissions = emissions.tolist()

# Ajouter les émissions selon le scénario choisi
for year in extended_years:
    if scenario == "Business as usual":
        new_emissions.append(new_emissions[-1])  # Émissions constantes après 2020
    elif scenario == "-2%/an":
        new_emissions.append(new_emissions[-1] * 0.98)  # Réduction de 2% par an
    elif scenario == "-5%/an":
        new_emissions.append(new_emissions[-1] * 0.95)  # Réduction de 5% par an

# Afficher les émissions avec distinction entre historique et scénario
st.title("Simulation des Émissions Anthropiques")
plt.figure()
plt.plot(annees, emissions, '-o', label="Émissions historiques (1850-2020)", color='blue')
plt.plot(extended_years, new_emissions[len(annees):], '-o', label=f"Scénario choisi (2020-2100): {scenario}", color='red')
plt.title("Émissions anthropiques : Historique et Scénarios")
plt.xlabel("Année")
plt.ylabel("Gt de Carbone / an")
plt.legend()
plt.grid()
st.pyplot(plt)

# Initialisation des réservoirs de carbone exprimé en tonne
P = [2300]  # Réservoir Terre (Gt)
A = [590]   # Réservoir Atmosphère (Gt)
E = [39000] # Réservoir Eau (Gt)
F = [0]     # Émissions anthropiques cumulées (GtC)
T = [0]     # Captage technologique (GtC)
temperature = [0.0]  # Température initiale (°C)
temps = [1850]       # Année de départ

# Curseurs pour ajuster les valeurs initiales
st.sidebar.header("Paramètres ajustables initiaux en 1850")
P[0] = st.sidebar.slider("Réservoir Terre (GtC)", 0, 5000, 2300, 10)
A[0] = st.sidebar.slider("Réservoir Atmosphère (GtC)", 0, 1000, 590, 10)
E[0] = st.sidebar.slider("Réservoir Océan (GtC)", 0, 100000, 39000, 1000)
F[0] = st.sidebar.slider("Émissions anthropiques cumulées (GtC)", 0.0, 10.0, 0.0, 0.1)
T[0] = st.sidebar.slider("Captage technologique (GtC)", 0.0, 10.0, 0.0, 0.1)

kt = st.sidebar.slider("Taux de captage technologique (%)", 0.0, 0.5, 0.0, step=0.1)
kp = st.sidebar.slider("Taux d'échange atmosphère → terre (%)", 0.0, 50.0, 20.3, step=0.1)
ke = st.sidebar.slider("Taux d'échange atmosphère → océan (%)", 0.0, 40.0, 15.6, step=0.1)
kr_land = st.sidebar.slider("Taux d'échange terre → atmosphère (%)", 98.0, 100.0, 99.0, step=0.1)
kr_water = st.sidebar.slider("Taux d'échange océan → atmosphère (%)", 97.00, 100.00, 99.77, step=0.01)
lambda_param = st.sidebar.slider("Constante de sensibilité climatique (°C/GtC)", 2.0, 6.0, 4.0, step=0.1)

# Simulation avec les données étendues
for i in range(len(annees_extended) - 1):
    # Flux anthropiques
    flux_from_anthropogenic = new_emissions[i]

    # Flux atmosphère vers autres réservoirs
    flux_to_land = kp * A[-1] / 100
    flux_to_water = ke * A[-1] / 100
    flux_to_tech = kt * A[-1] / 100

    # Flux réémis vers l'atmosphère
    flux_from_land = kr_land / 100 * flux_to_land
    flux_from_water = kr_water / 100 * flux_to_water

    # Mise à jour des réservoirs
    F.append(F[-1] + flux_from_anthropogenic)  # Émissions cumulées
    A.append(A[-1] + flux_from_anthropogenic - flux_to_land - flux_to_water - flux_to_tech + flux_from_land + flux_from_water)
    P.append(P[-1] + flux_to_land - flux_from_land)
    E.append(E[-1] + flux_to_water - flux_from_water)
    T.append(T[-1] + flux_to_tech)
    temperature.append(lambda_param * np.log(A[-1] / A[0]))
    temps.append(temps[-1] + 1)

# Synchronisation des longueurs
min_length = min(len(temps), len(A), len(F), len(P), len(E), len(T), len(temperature))
temps = temps[:min_length]
A = A[:min_length]
F = F[:min_length]
P = P[:min_length]
E = E[:min_length]
T = T[:min_length]
temperature = temperature[:min_length]

# Graphiques mis à jour avec les parties scénarios
st.title(f"Simulation des Scénarios : {scenario}")

# Réservoirs de carbone
plt.figure()
plt.plot(temps[:len(annees)], [val / A[0] * 100 for val in A[:len(annees)]], '-o', label="Atmosphère (1850-2020)", color='blue')
plt.plot(temps[len(annees):], [val / A[0] * 100 for val in A[len(annees):]], '-o', label="Atmosphère (2020-2100)", color='red')
plt.plot(temps[:len(annees)], [val / P[0] * 100 for val in P[:len(annees)]], '-o', label="Terre (1850-2020)", color='green')
plt.plot(temps[len(annees):], [val / P[0] * 100 for val in P[len(annees):]], '-o', label="Terre (2020-2100)", color='orange')
plt.plot(temps[:len(annees)], [val / E[0] * 100 for val in E[:len(annees)]], '-o', label="Océan (1850-2020)", color='purple')
plt.plot(temps[len(annees):], [val / E[0] * 100 for val in E[len(annees):]], '-o', label="Océan (2020-2100)", color='brown')
plt.title("Évolution des Réservoirs de CO2")
plt.xlabel("Année")
plt.ylabel("Variation de la Concentration de Carbone (%)")
plt.legend()
plt.grid()
st.pyplot(plt)

# Température globale
plt.figure()
plt.plot(temps[:len(annees)], temperature[:len(annees)], '-o', label="Température (1850-2020)", color='blue')
plt.plot(temps[len(annees):], temperature[len(annees):], '-o', label="Température (2020-2100)", color='red')
plt.title("Évolution de la Température Globale")
plt.xlabel("Année")
plt.ylabel("Température (°C)")
plt.grid()
plt.legend()
st.pyplot(plt)






