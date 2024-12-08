import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Modèle pour lavage individuel
def model_individual_with_period(mass_per_week, machine_cost=400, capacity=5, power_kw=1.0, cycle_duration_hr=1.0,
                                 co2_machine=100, lifetime_years=10, analysis_years=15):
    # Masse annuelle et totale sur la période d’analyse
    mass_per_year = mass_per_week * 52
    total_mass_analysis = mass_per_year * analysis_years

    # Cycles nécessaires
    cycles_per_week = np.ceil(mass_per_week / capacity)
    total_cycles = cycles_per_week * 52 * analysis_years

    # Énergie consommée par cycle
    energy_per_cycle = power_kw * cycle_duration_hr  # kWh
    energy_total = total_cycles * energy_per_cycle
    co2_total_energy = energy_total * 0.5  # CO2_PER_KWH

    # Bilan CO₂ fabrication machine (réparti sur la durée de vie réelle de la machine)
    co2_total_machine = co2_machine * (analysis_years / lifetime_years)
    energy_cost_total = energy_total * 0.15  # ENERGY_COST

    # Coût annuel amorti pour la machine
    annual_machine_cost = machine_cost / lifetime_years
    machine_cost_analysis = annual_machine_cost * analysis_years

    # Coût total
    total_cost = machine_cost_analysis + energy_cost_total
    total_co2 = co2_total_energy + co2_total_machine

    return {
        "cost_per_kg": total_cost / total_mass_analysis,
        "co2_per_kg": total_co2 / total_mass_analysis
    }

# Modèle pour lavage collectif
def model_service_with_period(num_clients, mass_per_client, machine_cost=20000, capacity=20, power_kw=2.0,
                              cycle_duration_hr=1.5, co2_machine=500, transport_distance=10, transport_mode="thermique",
                              personnel_cost=20000, personnel_years=10, van_cost=20000, van_co2=6000, van_lifetime=10,
                              machine_lifetime=30, carbon_tax=0, analysis_years=15):
    # Masse annuelle et totale sur la période d’analyse
    total_mass_per_week = num_clients * mass_per_client
    total_mass_analysis = total_mass_per_week * 52 * analysis_years

    # Cycles nécessaires
    cycles_per_week = np.ceil(total_mass_per_week / capacity)

    # Énergie consommée par cycle
    energy_per_cycle = power_kw * cycle_duration_hr  # kWh
    energy_total = cycles_per_week * energy_per_cycle * 52 * analysis_years
    co2_total_energy = energy_total * 0.5  # CO2_PER_KWH

    # Transport : caractéristiques selon le mode
    if transport_mode == "thermique":
        speed = 30  # km/h
        cost_per_km = 0.1
        co2_per_km = 0.2
        van_capacity = 500
        van_cost = 20000
        van_co2 = 6000
    elif transport_mode == "électrique":
        speed = 30  # km/h
        cost_per_km = 0.05
        co2_per_km = 0.05
        van_capacity = 500
        van_cost = 30000
        van_co2 = 4000
    elif transport_mode == "vélo":
        speed = 7  # km/h
        cost_per_km = 0.01
        co2_per_km = 0.005
        van_capacity = 50
        van_cost = 3000
        van_co2 = 100
    else:
        raise ValueError("Mode de transport inconnu.")

    # Trajets nécessaires
    trips_needed = np.ceil(total_mass_per_week / van_capacity)

    # Distance totale sur la période d’analyse
    total_distance_week = trips_needed * 2 * transport_distance  # aller-retour pour chaque trajet
    total_distance_analysis = total_distance_week * 52 * analysis_years
    co2_transport_total = total_distance_analysis * co2_per_km

    # Coût et bilan CO₂ camionnette/vélo
    van_cost_annual = van_cost / van_lifetime
    van_cost_analysis = van_cost_annual * analysis_years
    co2_total_van = van_co2 * (analysis_years / van_lifetime)

    # Bilan CO₂ fabrication machine (réparti sur la durée de vie réelle de la machine)
    co2_total_machine = co2_machine * (analysis_years / machine_lifetime)

    # Temps total de travail pour transport et lavage
    transport_time_per_week = total_distance_week / speed  # Temps en heures pour les trajets hebdomadaires
    washing_time_per_week = cycles_per_week * cycle_duration_hr  # Temps en heures pour les cycles de lavage
    total_time_per_week = transport_time_per_week + washing_time_per_week

    # Calcul du pourcentage d'emploi
    annual_hours = total_time_per_week * 52
    employment_rate = (annual_hours / (35 * 52)) * 100  # Pourcentage d'un temps plein (35h/semaine)

    # Taxe carbone
    total_co2 = co2_total_energy + co2_transport_total + co2_total_machine + co2_total_van
    carbon_tax_cost = total_co2 * carbon_tax / 1000

    # Coût total
    transport_cost_total = total_distance_analysis * cost_per_km
    cost_total_personnel = personnel_cost * (analysis_years / personnel_years)
    energy_cost_total = energy_total * 0.15  # ENERGY_COST
    total_cost = (machine_cost +
                  transport_cost_total +
                  energy_cost_total +
                  van_cost_analysis +
                  carbon_tax_cost +
                  cost_total_personnel)

    return {
        "cost_per_kg": total_cost / total_mass_analysis,
        "co2_per_kg": total_co2 / total_mass_analysis,
        "carbon_tax_cost": carbon_tax_cost,
        "total_distance_lifetime": total_distance_analysis,
        "employment_rate": employment_rate,  # Ajout de l'indicateur d'emploi
        "total_time_per_week": total_time_per_week  # Temps hebdomadaire total
    }

# Streamlit App
st.title("Comparaison des modèles de lavage : Paramètres et Graphiques interactifs")

# Inputs utilisateur
st.header("Étape 1 : Configurer les besoins")
mass_per_client = st.slider("Masse de linge par client (kg/semaine)", 4, 25, 10)
num_clients = st.slider("Nombre de clients", 1, 100, 10)
transport_mode = st.selectbox("Mode de transport", options=["thermique", "électrique", "vélo"])
transport_distance = st.slider("Distance moyenne aller-retour (km)", 1, 50, 10)

# Configurations avancées
st.sidebar.header("Paramètres avancés")
carbon_tax = st.sidebar.slider("Taxe carbone (€ / tonne de CO₂)", 0, 200, 50)

st.sidebar.markdown("### Lavage individuel")
machine_cost_ind = st.sidebar.slider("Prix d'une machine individuelle (€)", 200, 1000, 400)
capacity_ind = st.sidebar.slider("Capacité machine individuelle (kg/cycle)", 2, 8, 5)
power_kw_ind = st.sidebar.slider("Puissance machine individuelle (kW)", 0.5, 3.0, 1.0)
cycle_duration_ind = st.sidebar.slider("Durée du cycle individuel (heures)", 0.25, 2.0, 1.0)
co2_machine_ind = st.sidebar.slider("Bilan CO₂ machine individuelle (kg)", 50, 300, 100)
lifetime_years_ind = st.sidebar.slider("Durée de vie machine individuelle (années)", 5, 15, 10)

st.sidebar.markdown("### Lavage collectif")
machine_cost_serv = st.sidebar.slider("Prix d'une machine collective (€)", 5000, 50000, 20000)
capacity_serv = st.sidebar.slider("Capacité machine collective (kg/cycle)", 20, 100, 20)
power_kw_serv = st.sidebar.slider("Puissance machine collective (kW)", 1.0, 10.0, 2.0)
cycle_duration_serv = st.sidebar.slider("Durée du cycle collectif (heures)", 0.25, 2.0, 1.5)
co2_machine_serv = st.sidebar.slider("Bilan CO₂ machine collective (kg)", 200, 1000, 500)
personnel_cost = st.sidebar.slider("Coût annuel personnel (€)", 10000, 50000, 20000)

# Calculs
ind_results = model_individual_with_period(mass_per_client, machine_cost=machine_cost_ind, capacity=capacity_ind,
                                           power_kw=power_kw_ind, cycle_duration_hr=cycle_duration_ind,
                                           co2_machine=co2_machine_ind, lifetime_years=lifetime_years_ind)

serv_results = model_service_with_period(num_clients, mass_per_client, machine_cost=machine_cost_serv,
                                         capacity=capacity_serv, power_kw=power_kw_serv,
                                         cycle_duration_hr=cycle_duration_serv, co2_machine=co2_machine_serv,
                                         transport_distance=transport_distance, transport_mode=transport_mode,
                                         personnel_cost=personnel_cost, carbon_tax=carbon_tax)

# Affichage des résultats

st.header("Résultats Comparés")
st.write("### Lavage individuel")
st.write(f"Coût par kg : {ind_results['cost_per_kg']:.2f} €/kg")
st.write(f"Impact CO₂ par kg : {ind_results['co2_per_kg']:.2f} kg CO₂/kg")

st.write("### Lavage collectif")
st.write(f"Coût par kg : {serv_results['cost_per_kg']:.2f} €/kg")
st.write(f"Impact CO₂ par kg : {serv_results['co2_per_kg']:.2f} kg CO₂/kg")
st.write(f"Taxe carbone totale : {serv_results['carbon_tax_cost']:.2f} €")
st.write(f"Distance totale sur la durée de vie : {serv_results['total_distance_lifetime']:.2f} km")
st.write(f"Taux d'emploi : {serv_results['employment_rate']:.2f}%")
st.write(f"Temps hebdomadaire total (transport + lavage) : {serv_results['total_time_per_week']:.2f} heures")
# Graphiques interactifs
st.header("Graphiques interactifs")
fig = go.Figure()

# Ajout des barres pour le lavage individuel
fig.add_trace(go.Bar(name="Individuel", x=["Coût (€ / kg)", "CO₂ (kg / kg)"],
                     y=[ind_results["cost_per_kg"], ind_results["co2_per_kg"]]))

# Ajout des barres pour le lavage collectif
fig.add_trace(go.Bar(name="Collectif", x=["Coût (€ / kg)", "CO₂ (kg / kg)"],
                     y=[serv_results["cost_per_kg"], serv_results["co2_per_kg"]]))

fig.update_layout(title="Comparaison des modèles",
                  xaxis_title="Indicateurs",
                  yaxis_title="Valeurs",
                  barmode="group")

st.plotly_chart(fig)
