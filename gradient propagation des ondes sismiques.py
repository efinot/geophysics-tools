import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Titre principal
st.title("Simulation de la Propagation des Ondes Sismiques")
st.markdown("""
Cette application interactive vous permet de visualiser et d'explorer la propagation des **ondes sismiques** (ondes P et S) dans différents milieux.
""")

# **Paramètres utilisateur**
st.sidebar.header("Configuration des Ondes")
wave_type = st.sidebar.radio("Type d'Onde", ["Ondes P (primaires)", "Ondes S (secondaires)"])
material = st.sidebar.selectbox("Milieu traversé", ["Roche (granite)", "Sédiments (sable)", "Eau", "Air"])
time_steps = st.sidebar.slider("Nombre d'étapes temporelles", min_value=10, max_value=100, value=50)
grid_size = st.sidebar.slider("Taille de la grille (pixels)", min_value=50, max_value=200, value=100)

# Vitesse des ondes par milieu et type
velocities = {
    "Ondes P (primaires)": {"Roche (granite)": 6000, "Sédiments (sable)": 1500, "Eau": 1450, "Air": 340},
    "Ondes S (secondaires)": {"Roche (granite)": 3500, "Sédiments (sable)": 700, "Eau": 0, "Air": 0},
}

# Obtenez la vitesse correspondante
v = velocities[wave_type][material]

# Gestion des cas où les ondes S ne se propagent pas
if v == 0:
    st.error(f"Les {wave_type} ne se propagent pas dans {material}. Veuillez choisir une autre configuration.")
else:
    st.write(f"**Vitesse des {wave_type} dans {material}** : {v} m/s")

    # **Simulation de la propagation**
    st.markdown("## Visualisation : Propagation des Ondes")
    x = np.linspace(0, grid_size, grid_size)
    y = np.linspace(0, grid_size, grid_size)
    X, Y = np.meshgrid(x, y)

    # Fonction pour calculer le champ d'onde
    def compute_wave(t, v):
        return np.sin(2 * np.pi * (X + Y - v * t / grid_size))

    # Animation avec Matplotlib
    fig, ax = plt.subplots(figsize=(6, 6))
    wave_field = compute_wave(0, v)
    im = ax.imshow(wave_field, cmap="seismic", extent=[0, grid_size, 0, grid_size], origin="lower")
    ax.set_title(f"Propagation des {wave_type}")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Distance (m)")

    def update(frame):
        wave_field = compute_wave(frame, v)
        im.set_data(wave_field)
        return [im]

    ani = animation.FuncAnimation(fig, update, frames=time_steps, interval=100, blit=True)
    st.pyplot(fig)

    # Comparaison des vitesses
    st.markdown("### Comparaison des Vitesses dans Différents Milieux")
    materials = ["Roche (granite)", "Sédiments (sable)", "Eau", "Air"]
    p_velocities = [velocities["Ondes P (primaires)"][mat] for mat in materials]
    s_velocities = [velocities["Ondes S (secondaires)"][mat] for mat in materials]

    x = np.arange(len(materials))
    width = 0.35
    fig, ax = plt.subplots()
    ax.bar(x - width / 2, p_velocities, width, label="Ondes P")
    ax.bar(x + width / 2, s_velocities, width, label="Ondes S")
    ax.set_ylabel("Vitesse (m/s)")
    ax.set_title("Comparaison des Vitesses d'Ondes")
    ax.set_xticks(x)
    ax.set_xticklabels(materials)
    ax.legend()
    st.pyplot(fig)

    # Ajout d'une carte interactive pour visualiser la distance entre l'épicentre et la station
    st.markdown("### Visualisation Épicentre-Station")
    epicenter_x = st.slider("Position de l'épicentre sur X (m)", 0, grid_size, grid_size // 2)
    epicenter_y = st.slider("Position de l'épicentre sur Y (m)", 0, grid_size, grid_size // 2)
    station_x = st.slider("Position de la station sur X (m)", 0, grid_size, grid_size // 3)
    station_y = st.slider("Position de la station sur Y (m)", 0, grid_size, grid_size // 3)

    distance = np.sqrt((station_x - epicenter_x)**2 + (station_y - epicenter_y)**2)
    arrival_time = distance / v

    st.write(f"**Distance entre l'épicentre et la station** : {distance:.2f} m")
    st.write(f"**Temps d'arrivée estimé** : {arrival_time:.2f} secondes")

    # Théorie et explications
    st.markdown("""
    ### Théorie : Ondes Sismiques
    - **Ondes P (primaires)** :
        - Propagation par compression et dilatation.
        - Vitesse la plus rapide, traversant solides, liquides et gaz.
    - **Ondes S (secondaires)** :
        - Propagation par cisaillement.
        - Plus lentes et incapables de traverser les liquides ou gaz.
    """)

    # Téléchargement des résultats
    st.sidebar.header("Téléchargement des Données")
    if st.sidebar.button("Télécharger les données des vitesses"):
        import pandas as pd
        data = {
            "Matériau": materials,
            "Vitesse des Ondes P (m/s)": p_velocities,
            "Vitesse des Ondes S (m/s)": s_velocities,
        }
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)
        st.sidebar.download_button(
            label="Télécharger CSV",
            data=csv,
            file_name="vitesses_ondes_sismiques.csv",
            mime="text/csv"
        )
