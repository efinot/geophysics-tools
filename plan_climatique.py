import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Paramètres globaux ajustables par l'utilisateur
st.sidebar.header("Paramètres globaux")
years = st.sidebar.slider("Durée de la simulation (années)", 10, 50, 30)
paris_target = st.sidebar.slider("Réduction cible (%)", 10, 100, 50)
PIB_INITIAL = st.sidebar.number_input("Chiffre d'affaires initial (k€)", min_value=10, max_value=10000, value=3000)
PIB_GROWTH = st.sidebar.number_input("Croissance économique (%)", min_value=-1.0, max_value=5.0, value=2.0) / 100
INVESTMENT_THRESHOLD = st.sidebar.slider("Seuil d'investissement (% du CA)", -3, 5, 2)

# Secteurs à modéliser
sectors = ["Transport", "Électricité", "Chauffage", "Achats", "Numérique"]

# Fonction pour simuler les émissions et les coûts
def simulate_emissions_and_costs(
    initial_emissions, reductions, durations, investment_per_sector
):
    yearly_data = []
    current_emissions = initial_emissions.copy()
    total_investments = 0
    total_reductions = 0
    yearly_pib = PIB_INITIAL

    for year in range(1, years + 1):
        yearly_emissions = 0
        yearly_investment = 0
        reductions_by_sector = {}

        for sector, share in current_emissions.items():
            if year <= durations[sector]:
                reduction = reductions[sector] / 100
                sector_emissions = share * (1 - reduction)
                yearly_emissions += sector_emissions
                yearly_investment += investment_per_sector[sector] * reduction * share
                reductions_by_sector[sector] = share * reduction
                current_emissions[sector] = sector_emissions
                total_reductions += share * reduction
            else:
                yearly_emissions += share
                reductions_by_sector[sector] = 0

        investment_ratio = (yearly_investment / yearly_pib) * 100  # Calcul du ratio investissement / CA
        yearly_data.append({
            "Year": year,
            "Emissions (tonnes de CO₂)": yearly_emissions,
            "Yearly Investment (k€)": yearly_investment,
            "Investment / CA (%)": investment_ratio,
            "PIB (k€)": yearly_pib,
            **reductions_by_sector,
        })
        total_investments += yearly_investment
        yearly_pib *= (1 + PIB_GROWTH)  # Augmentation annuelle du CA

    cost_per_tonne = total_investments / total_reductions if total_reductions > 0 else float('inf')
    return pd.DataFrame(yearly_data), total_investments, cost_per_tonne

# Demander la quantité totale initiale d'émissions
st.sidebar.header("Quantité totale initiale de carbone")
total_initial_emissions = st.sidebar.number_input(
    "Quantité totale d'émissions (tonnes de CO₂)", min_value=1, max_value=100, value=10
)

# Répartition des émissions par secteur
st.sidebar.header("Répartition initiale des émissions (%)")
sector_emissions = {}
for sector in sectors:
    percentage = st.sidebar.slider(f"{sector} (%)", 0, 100, 20)
    sector_emissions[sector] = (percentage / 100) * total_initial_emissions

# Paramètres des efforts par secteur
st.sidebar.header("Efforts par secteur")
sector_reductions = {}
effort_durations = {}
investment_per_sector = {}

for sector in sectors:
    st.sidebar.markdown(f"### {sector}")
    reduction = st.sidebar.slider(f"Niveau d'effort annuel {sector} (%)", 0.0, 10.0, 5.0)
    duration = st.sidebar.slider(f"Durée de l'effort {sector} (années)", 1, years, 15)
    investment = st.sidebar.slider(f"Investissement annuel {sector} (k€)", 0, 100, 50)
    sector_reductions[sector] = reduction
    effort_durations[sector] = duration
    investment_per_sector[sector] = investment

# Simulation
results, total_investments, cost_per_tonne = simulate_emissions_and_costs(
    sector_emissions, sector_reductions, effort_durations, investment_per_sector
)

# Graphique : Réduction des émissions par secteur (en couleur)
st.header("Réductions cumulées par secteur au fil des années")
fig_reductions = go.Figure()

for sector in sectors:
    fig_reductions.add_trace(go.Scatter(
        x=results["Year"],
        y=results[sector],
        mode='lines',
        stackgroup='one',  # Aire empilée
        name=f"Réduction {sector}"
    ))

fig_reductions.update_layout(
    title="Réduction cumulée des émissions par secteur (tonnes de CO₂)",
    xaxis_title="Année",
    yaxis_title="Réductions (tonnes de CO₂)",
    showlegend=True
)
st.plotly_chart(fig_reductions)

# Graphique : Émissions totales
st.header("Évolution des émissions résiduelles totales")
fig_emissions = go.Figure()
fig_emissions.add_trace(go.Scatter(x=results["Year"], y=results["Emissions (tonnes de CO₂)"], mode='lines+markers', name="Émissions résiduelles"))
fig_emissions.update_layout(title="Émissions résiduelles après réductions", xaxis_title="Année", yaxis_title="Émissions (tonnes de CO₂)")
st.plotly_chart(fig_emissions)

# Graphique : Efforts financiers cumulés
st.header("Efforts financiers cumulés par année")
fig_investments = go.Figure()
fig_investments.add_trace(go.Scatter(
    x=results["Year"],
    y=results["Yearly Investment (k€)"].cumsum(),
    mode='lines+markers',
    name="Investissements cumulés (k€)"
))
fig_investments.update_layout(
    title="Impact éco cumulés pour atteindre les objectifs",
    xaxis_title="Année",
    yaxis_title="Investissements cumulés (k€)",
)
st.plotly_chart(fig_investments)

# Graphique : Ratio investissement / CA
st.header("Ratio Impact éco / Chiffre d'Affaires par Année")
fig_investment_ratio = go.Figure()
fig_investment_ratio.add_trace(go.Scatter(
    x=results["Year"],
    y=results["Investment / CA (%)"],
    mode='lines+markers',
    name="Ratio Investissement / CA"
))
fig_investment_ratio.update_layout(
    title="Impact éco en pourcentage du CA",
    xaxis_title="Année",
    yaxis_title="Ratio Impact éco / CA (%)",
)
st.plotly_chart(fig_investment_ratio)

# Vérification du seuil d'investissement
max_ratio = results["Investment / CA (%)"].max()
if max_ratio > INVESTMENT_THRESHOLD:
    st.warning(f"⚠️ Le ratio investissement / CA dépasse le seuil acceptable ({INVESTMENT_THRESHOLD}%) dans certaines années.")

# Indicateurs économiques
st.header("Indicateurs économiques")
st.write(f"**Coût total de l impact éco  (k€) :** {total_investments:.2f} k€")
st.write(f"**Coût (k€) par tonne de CO₂ évitée :** {cost_per_tonne:.2f} €/tCO₂")

# Indicateur de performance climatique
final_emissions = results["Emissions (tonnes de CO₂)"].iloc[-1]
achievement = "✅ Objectif atteint" if final_emissions <= total_initial_emissions * (1 - paris_target / 100) else "❌ Objectif non atteint"
st.write(f"**Statut climatique :** {achievement}")
