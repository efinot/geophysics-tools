import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Titre de l'application
st.title("Analyse du Gradient Géothermique")

# Description de l'application
st.markdown("""
Cette application permet d'explorer les profils thermiques mesurés dans des forages profonds
et de calculer le gradient géothermique. Interagissez avec les paramètres pour comprendre
comment la température varie avec la profondeur.
""")

# Entrée utilisateur pour les paramètres
st.sidebar.header("Paramètres")
gradient = st.sidebar.slider("Gradient géothermique (°C/km)", 20, 50, 30, step=1)
temp_surface = st.sidebar.number_input("Température à la surface (°C)", value=15)
profondeur_max = st.sidebar.slider("Profondeur maximale (m)", 1000, 10000, 5000, step=100)

# Génération des données
profondeurs = np.linspace(0, profondeur_max, 100)
temperatures = temp_surface + (gradient / 1000) * profondeurs

# Affichage des données sous forme de tableau
st.subheader("Données simulées")
data = pd.DataFrame({
    "Profondeur (m)": profondeurs,
    "Température (°C)": temperatures
})
st.dataframe(data)

# Graphique interactif
st.subheader("Graphique du profil thermique")
fig, ax = plt.subplots()
ax.plot(temperatures, profondeurs, label=f"Gradient : {gradient} °C/km")
ax.set_xlabel("Température (°C)")
ax.set_ylabel("Profondeur (m)")
ax.invert_yaxis()  # Inverser l'axe pour représenter la profondeur
ax.legend()
st.pyplot(fig)

# Calculs supplémentaires
st.subheader("Calcul du Gradient Géothermique")
temp_gradient = np.gradient(temperatures, profondeurs)
st.write("Gradient thermique moyen :", round(temp_gradient.mean(), 2), "°C/m")

# Exemple réel
st.subheader("Comparaison avec des données réelles")
st.markdown("""
Les gradients géothermiques varient selon les régions géologiques. Environnements typiques :
- **Crustale stable** : 20-30 °C/km
- **Zones volcaniques actives** : > 40 °C/km
""")
