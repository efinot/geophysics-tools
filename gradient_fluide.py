import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from io import StringIO

# Titre de l'application
st.title("Simulation du Mouvement des Fluides Souterrains")
st.markdown(r"""
Explorez les effets des paramètres physiques sur le mouvement des fluides souterrains en milieu poreux. Basé sur la **loi de Darcy** :

$$
Q = \frac{k \cdot \Delta P \cdot S}{\eta \cdot L}
$$
""", unsafe_allow_html=True)






# Choix du matériau
st.sidebar.header("Sélection du matériau")
material = st.sidebar.selectbox(
    "Type de matériau",
    options=["Sable", "Gravier", "Argile", "Roche poreuse"],
    index=0
)
material_properties = {
    "Sable": 1e-12,
    "Gravier": 1e-10,
    "Argile": 1e-14,
    "Roche poreuse": 1e-13,
}
k = material_properties[material]

# Entrées utilisateur
st.sidebar.header("Paramètres physiques")
delta_p = st.sidebar.slider("Différence de pression (ΔP) en Pa", min_value=1.0, max_value=10000.0, value=1000.0)

S = st.sidebar.slider("Surface (S) en m²", min_value=0.1, max_value=10.0, value=1.0)
L = st.sidebar.slider("Longueur traversée (L) en m", min_value=0.1, max_value=100.0, value=10.0)

# Ajouter un champ de saisie pour la viscosité dynamique
eta = st.sidebar.number_input(
    "Viscosité dynamique (η) en Pa·s",
    min_value=1e-6,  # Viscosité minimale
    max_value=10.0,  # Viscosité maximale
    value=1e-3,      # Viscosité par défaut (eau)
    format="%.1e"    # Affichage en notation scientifique
)
st.sidebar.write(f"Viscosité dynamique (η) : {eta:.1e} Pa·s")

# Calcul du débit volumique
Q = (k * delta_p * S) / (eta * L)

# Affichage des résultats
st.write("### Résultats")
st.write(f"**Matériau sélectionné :** {material}")
st.write(f"**Perméabilité (k) :** {k:.1e} m²")
st.write(f"**Débit volumique calculé (Q) :** {Q:.2e} m³/s")

# Génération de données pour le téléchargement
data = {
    "Paramètre": ["Perméabilité (k)", "Différence de pression (ΔP)", "Viscosité (η)", "Surface (S)", "Longueur (L)", "Débit (Q)"],
    "Valeur": [k, delta_p, eta, S, L, Q],
    "Unité": ["m²", "Pa", "Pa·s", "m²", "m", "m³/s"]
}
df = pd.DataFrame(data)

# Option de téléchargement
csv = StringIO()
df.to_csv(csv, index=False)
st.download_button(
    label="Télécharger les résultats (CSV)",
    data=csv.getvalue(),
    file_name="resultats_fluides_souterrains.csv",
    mime="text/csv"
)

# Graphique interactif
st.write("### Débit en fonction d'un paramètre variable")
variable = st.selectbox("Choisissez une variable à analyser :", ["Perméabilité (k)", "Pression (ΔP)", "Longueur (L)"])

if variable == "Perméabilité (k)":
    k_values = np.logspace(-14, -10, 100)
    Q_values = (k_values * delta_p * S) / (eta * L)

    # Premier graphe linéaire
    st.markdown("### Graphique linéaire")
    fig1, ax1 = plt.subplots()
    ax1.plot(k_values, Q_values, label="Q vs k")
    ax1.set_xlabel("Perméabilité (m2)")
    ax1.set_ylabel("Débit (m³/s)")
    ax1.legend()
    st.pyplot(fig1)


    # Second graphe log-log
    st.markdown("### Graphique log-log")
    fig2, ax2 = plt.subplots()
    ax2.loglog(k_values, Q_values, label="Q vs k(log-log)", color='orange')
    ax2.set_xlabel("Perméabilité (m2)")
    ax2.set_ylabel("Débit (m³/s)")
    ax2.legend()
    st.pyplot(fig2)
    pass


elif variable == "Pression (ΔP)":
    delta_p_values = np.linspace(1, 10000, 100)
    Q_values = (k * delta_p_values * S) / (eta * L)
    # Premier graphe linéaire
    st.markdown("### Graphique linéaire")
    fig1, ax1 = plt.subplots()
    ax1.plot(delta_p_values, Q_values, label="Q vs ΔP")
    ax1.set_xlabel("Différence de pression (ΔP) [Pa]")
    ax1.set_ylabel("Débit (m³/s)")
    ax1.legend()
    st.pyplot(fig1)

    # Second graphe log-log
    st.markdown("### Graphique log-log")
    fig2, ax2 = plt.subplots()
    ax2.loglog(delta_p_values, Q_values, label="Q vs ΔP(log-log)", color='orange')
    ax2.set_xlabel("Différence de pression (ΔP) [Pa]")
    ax2.set_ylabel("Débit (m³/s)")
    ax2.legend()
    st.pyplot(fig2)
    pass


    
elif variable == "Longueur (L)":
    L_values = np.linspace(0.1, 100, 100)
    Q_values = (k * delta_p * S) / (eta * L_values)

    # Premier graphe linéaire
    st.markdown("### Graphique linéaire")
    fig1, ax1 = plt.subplots()
    ax1.plot(L_values, Q_values, label="Q vs L")
    ax1.set_xlabel("Longueur traversée (L) [m]")
    ax1.set_ylabel("Débit (m³/s)")
    ax1.legend()
    st.pyplot(fig1)

    # Second graphe log-log
    st.markdown("### Graphique log-log")
    fig2, ax2 = plt.subplots()
    ax2.loglog(L_values, Q_values, label="Q vs L (log-log)", color='orange')
    ax2.set_xlabel("Longueur traversée (L) [m]")
    ax2.set_ylabel("Débit (m³/s)")
    ax2.legend()
    st.pyplot(fig2)
pass

