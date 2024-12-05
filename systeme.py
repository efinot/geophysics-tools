import streamlit as st
import plotly.graph_objects as go

# --- Entrées utilisateur ---
st.sidebar.header("Paramètres de la chaîne de production")

# Flux initiaux
input_material_a = st.sidebar.number_input("Matière première  Bioproduction (kg)", min_value=0.0, max_value=50.0,value=10.0)
input_material_b = st.sidebar.number_input("Matière première  Purification  (kg)", min_value=0.0,max_value=50.0, value=1.0)
input_material_c = st.sidebar.number_input("Matière première  Galénique (kg)", min_value=0.0,max_value=50.0, value=0.1)
input_energy_a = st.sidebar.number_input("Énergie Bioproduction (kWh)", min_value=0.0, max_value=1000.0,value=500.0)
input_energy_b = st.sidebar.number_input("Énergie Purification (kWh)", min_value=0.0, max_value=100.0,value=50.0)
input_energy_c = st.sidebar.number_input("Énergie Galénique (kWh)", min_value=0.0, max_value=100.0,value=20.0)

# Sous-systèmes
st.sidebar.subheader("Sous-système A : Bioproduction")
efficiency_a_material = st.sidebar.slider("Efficacité matière (%)", min_value=0.0, max_value=100.0,value=40.0)
efficiency_a_energy = st.sidebar.slider("Efficacité énergétique (%)", min_value=0.0,max_value=100.0, value=60.0)

st.sidebar.subheader("Sous-système B : Purification")
efficiency_b_material = st.sidebar.slider("Efficacité matière (%)", min_value=0.0,max_value=100.0, value=90.0)
efficiency_b_energy = st.sidebar.slider("Efficacité énergétique (%)", min_value=0.0,max_value=100.0, value=50.0)

st.sidebar.subheader("Sous-système C : Galénique")
efficiency_c_material = st.sidebar.slider("Efficacité matière (%)", min_value=0.0,max_value=100.0, value=90.0,key="efficiency_c_material")
efficiency_c_energy = st.sidebar.slider("Efficacité énergétique (%)", min_value=0.0,max_value=100.0, value=70.0,key="efficiency_c_energy")


# Recyclage
st.sidebar.subheader("Recyclage")
recycling_rate_material = st.sidebar.slider("Taux de recyclage matière (%)", 0, 100, 10,key="recycling_rate_material")
recycling_rate_energy = st.sidebar.slider("Taux de recyclage énergie (%)", 0, 100, 50,key="recycling_rate_energy")

# Impacts environnementaux et coûts
st.sidebar.subheader("Impact environnemental et coûts")
co2_per_kwh = st.sidebar.number_input("CO₂ par kWh (kg)", min_value=0.0 , max_value=100.0,value=0.233,key="co2_per_kwh")
co2_per_kg_material = st.sidebar.number_input("g de CO2 par kg de matière ", min_value=0.0 , max_value=100.0 , value=32.0,key="co2_per_kg_material")
cost_per_kwh = st.sidebar.number_input("Coût (€) par kWh ", min_value=0.0, max_value=100.0, value=0.25,key="cost_per_kwh")
cost_per_kg_material = st.sidebar.number_input("Coût (€) par kg de matière ", min_value=0.0, max_value=100.0, value=5.0,key="cost_per_kg_material")

# --- Calculs dynamiques ---
# Sous-système A : Bioproduction
material_a_output = input_material_a * (efficiency_a_material / 100)
energy_a_output = input_energy_a * (1-efficiency_a_energy / 100)


# Sous-système B : Purification
material_b_output = (material_a_output+input_material_b) * (efficiency_b_material / 100)
energy_b_output = input_energy_b * (1-efficiency_b_energy / 100)


# Sous-système C : Galénique
material_c_output = (material_b_output + input_material_c) * (efficiency_c_material / 100)
energy_c_output = input_energy_c * (1-efficiency_c_energy / 100)


# Pertes et recyclage
energy_input=input_energy_a+input_energy_b+input_energy_c
energy_loss = energy_a_output+energy_b_output+energy_c_output
recycled_energy = energy_loss * (recycling_rate_energy / 100)

material_input=input_material_a+input_material_b+input_material_c
material_loss = material_input - material_c_output
recycled_material = material_loss * (recycling_rate_material / 100)

# Impacts environnementaux


# Calcul des émissions carbone

co2_energy =(energy_input-recycled_energy)* co2_per_kwh
co2_material =(material_input-recycled_material)* co2_per_kg_material


total_co2 = co2_energy + co2_material 
total_cost = (energy_input-recycled_energy)*cost_per_kwh + (material_input-recycled_material)*cost_per_kg_material

perf_co2=material_c_output/total_co2/0.001
perf_cout=total_cost/material_c_output

# --- Résultats ---
st.header("Résultats")

st.write(f"**Masse de Produit final utile (kg) :** {material_c_output:.2f}")
st.write(f"**Masse de Produit intrant (kg) :** {material_input:.2f}")
st.write(f"**Pertes totales d'énergie (kWh) :** {energy_loss-recycled_energy:.2f}")
st.write(f"**Émissions de CO₂ (g) :** {total_co2:.2f}")
st.write(f"**Coût total de production (€) :** {total_cost:.2f}")
st.write(f"**Masse produite / CO2 :** {perf_co2:.2f}")
st.write(f"**cout (€) / Masse produite (kg) :** {perf_cout:.2f}")

# --- Diagramme de Sankey ---
st.subheader("Diagramme des flux")

labels = [
    "Énergie", "Matière",
    "Bioproduction", "Purification", "Galénique",
    "Produit final", "Perte énergie"
]

sources = [0, 0, 0, 1, 1, 1, 2, 3, 4, 2, 3, 4, 5, 6]
targets = [2, 3, 4, 2, 3, 4, 3, 4, 5, 6, 6, 6, 1, 0]
values = [
    input_energy_a, input_energy_b, input_energy_c,
    input_material_a*50, input_material_b*50, input_material_c*50,
    material_a_output*50, material_b_output*50, material_c_output*50,
    energy_a_output, energy_b_output, energy_c_output,
    recycled_material*100, recycled_energy
]




fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color=[
            "#ff7f0e",  # Énergie (orange)
            "#2ca02c",  # Bioproduction (vert)
            "#17becf",  # Sous-produit C (cyan)
            "#17becf",  # Sous-produit C (cyan)
            "#17becf",  # Sous-produit C (cyan)
            "#2ca02c",  # Bioproduction (vert)
            "#ff7f0e"   # Énergie (orange)
        ],
        # Ajout d'options hoverlabel si nécessaire
        hoverlabel=dict(
            font=dict(size=16, color="black")  # Taille et couleur du texte au survol
        )
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=[
            "#ff7f0e",  # Énergie (orange)
            "#ff7f0e",  # Énergie (orange)
            "#ff7f0e",  # Énergie (orange)
            "#2ca02c",  # Bioproduction (vert)
            "#2ca02c",  # Bioproduction (vert)
            "#2ca02c",  # Bioproduction (vert)
            "#2ca02c",  # Bioproduction (vert)
            "#2ca02c",  # Bioproduction (vert)
            "#2ca02c",  # Bioproduction (vert)
            "#ff7f0e",  # Énergie (orange)
            "#ff7f0e",  # Énergie (orange)
            "#ff7f0e",  # Énergie (orange)
            "#7f7f7f",  # Recyclage énergie (gris)
            "#7f7f7f"   # Recyclage énergie (gris)
        ]
    )
))

# Mettez à jour la taille et la couleur du texte via la configuration globale
fig.update_layout(
    title_text="Chaîne de production : Bioproduction, Purification, Galénique avec Recyclage",
    font=dict(size=20, color="black"),  # Augmente la taille du texte
    height=700,
    paper_bgcolor="white",  # Fond blanc
    plot_bgcolor="white"    # Fond de la zone graphique en blanc
)

st.plotly_chart(fig, use_container_width=True)




