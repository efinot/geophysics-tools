import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from io import StringIO

# Titre de l'application
st.title("Simulation du Mouvement des Fluides Souterrains")
st.markdown("""
Explorez les effets des paramètres physiques sur le mouvement des fluides souterrains en milieu poreux. Basé sur la **loi de Darcy** :
$$ Q = \\frac{k \cdot \\Delta P \cdot S}{\\eta \cdot L} $$
""")

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
eta = st.sidebar.slider("Viscosité dynamique (η) en Pa·s", min_value=1e-4, max_value=1e-2, value=1e-3, format="%.1e")
S = st.sidebar.slider("Surface (S) en m²", min_value=0.1, max_value=10.0, value=1.0)
L = st.sidebar.slider("Longueur traversée (L) en m", min_value=0.1, max_value=100.0, value=10.0)

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
    plt.plot(k_values, Q_values)
    plt.xscale("log")
    plt.xlabel("Perméabilité (k) [m²]")
    plt.ylabel("Débit volumique (Q) [m³/s]")
    plt.title("Débit en fonction de la perméabilité")
elif variable == "Pression (ΔP)":
    delta_p_values = np.linspace(1, 10000, 100)
    Q_values = (k * delta_p_values * S) / (eta * L)
    plt.plot(delta_p_values, Q_values)
    plt.xlabel("Différence de pression (ΔP) [Pa]")
    plt.ylabel("Débit volumique (Q) [m³/s]")
    plt.title("Débit en fonction de la différence de pression")
elif variable == "Longueur (L)":
    L_values = np.linspace(0.1, 100, 100)
    Q_values = (k * delta_p * S) / (eta * L_values)
    plt.plot(L_values, Q_values)
    plt.xlabel("Longueur traversée (L) [m]")
    plt.ylabel("Débit volumique (Q) [m³/s]")
    plt.title("Débit en fonction de la longueur")

# Affichage du graphique
st.pyplot(plt)

# Simulation dynamique
st.write("### Simulation dynamique")
grid_size = 20
fluid_grid = np.zeros((grid_size, grid_size))
x, y = np.meshgrid(np.arange(grid_size), np.arange(grid_size))

def update(frame):
    global fluid_grid
    fluid_grid = (fluid_grid + np.random.normal(0, 0.1, fluid_grid.shape)).clip(0, 1)
    plt.clf()
    plt.imshow(fluid_grid, cmap="Blues", origin="lower")
    plt.title("Simulation du mouvement des fluides")
    plt.colorbar(label="Intensité du flux")

ani = animation.FuncAnimation(plt.gcf(), update, frames=100, interval=100)
st.pyplot(plt)

st.markdown("""
- **Perméabilité (k)** : Milieux très perméables favorisent un flux rapide.
- **Pression (ΔP)** : L'augmentation de la pression augmente le débit.
- **Longueur (L)** : Plus la distance augmente, plus le débit diminue.
""")

