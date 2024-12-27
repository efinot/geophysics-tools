

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import streamlit as st



DEFAULT_ALPHA = 0.1
DEFAULT_BETA = 0.05
DEFAULT_GAMMA = 0.1
DEFAULT_DELTA = 0.08
DEFAULT_ETA = 0.03
DEFAULT_RHO = 0.2
DEFAULT_SIGMA = 0.1
DEFAULT_KAPPA = 0.05
DEFAULT_LAMBDA = 0.07
DEFAULT_MU = 0.09
DEFAULT_NU = 0.04
DEFAULT_NONLIN = 0.1

# Conditions initiales
DEFAULT_E0 = 1.0  # Initial Energy
DEFAULT_M0 = 1.0  # Initial Matter
DEFAULT_R0 = 1.0  # Initial Resources
DEFAULT_S0 = 1.0  # Initial Entropy

# Temps
DEFAULT_START_TIME = 0
DEFAULT_END_TIME = 100
DEFAULT_TIME_POINTS = 500

def initialize_parameters():
    return {
        "alpha": DEFAULT_ALPHA,
        "beta": DEFAULT_BETA,
        "gamma": DEFAULT_GAMMA,
        "delta": DEFAULT_DELTA,
        "eta": DEFAULT_ETA,
        "rho": DEFAULT_RHO,
        "sigma": DEFAULT_SIGMA,
        "kappa": DEFAULT_KAPPA,
        "lambda": DEFAULT_LAMBDA,
        "mu": DEFAULT_MU,
        "nu": DEFAULT_NU,
        "nonlin": DEFAULT_NONLIN,
        "E0": DEFAULT_E0,
        "M0": DEFAULT_M0,
        "R0": DEFAULT_R0,
        "S0": DEFAULT_S0,
        "start_time": DEFAULT_START_TIME,
        "end_time": DEFAULT_END_TIME,
        "time_points": DEFAULT_TIME_POINTS,
    }
params = initialize_parameters()


# Define the system of equations
def system_equations(t, y, params):
    E, M, R, S = y  # State variables
    alpha, beta, gamma, delta, eta, rho, sigma, kappa, lambda_, mu, nu, nonlin = params  # Parameters

    # Differential equations with non-linear feedback
    dE_dt = -alpha * M - beta * S - gamma * R - nonlin * E**2
    dM_dt = delta * E + eta * R - nonlin * M**2
    dR_dt = rho * E + sigma * M + kappa * S + nonlin * R**2
    dS_dt = +lambda_ * M + mu * E + nu * R + nonlin * S**2

   # Ensure values remain within bounds
    E = max(0, min(4 * params[-4], E))  # Energy capped at 4x initial
    M = max(0, min(4 * params[-3], M))  # Matter capped at 4x initial
    R = max(0, min(4 * params[-2], R))  # Resources capped at 4x initial
    S = max(0, min(5 * params[-2], S))  # Entropy can decrease but not go negative
    
    return [dE_dt, dM_dt, dR_dt, dS_dt]



# Streamlit app setup
st.title("Decarbonation System Simulation")
st.markdown("This app simulates the dynamics of a decarbonation system with energy, matter, resources, and entropy.")

# Display the equations
st.header("Equations Simulated")
st.latex(r"""
\frac{dE}{dt} = -\alpha M - \beta S - \gamma R - \omega E^2
""")
st.latex(r"""
\frac{dM}{dt} = \delta E + \eta R- \omega M^2
""")
st.latex(r"""
\frac{dR}{dt} = \rho E + \sigma M + \kappa S+ \omega R
""")
st.latex(r"""
\frac{dS}{dt} = \lambda M + \mu E + \nu R + \omega S
""")



# Sidebar for parameters
st.sidebar.header("Adjust Parameters")
alpha = st.sidebar.slider("Alpha (Energy-Matter)", 0.01, 0.5, 0.1, 0.01)
beta = st.sidebar.slider("Beta (Energy-Entropy)", 0.01, 0.5, 0.1, 0.01)
gamma = st.sidebar.slider("Gamma (Energy-Resources)", 0.01, 0.5, 0.1, 0.01)
delta = st.sidebar.slider("Delta (Matter-Energy)", 0.01, 0.5, 0.1, 0.01)
eta = st.sidebar.slider("Eta (Matter-Resources)", 0.01, 0.5, 0.1, 0.01)
rho = st.sidebar.slider("Rho (Resources-Energy)", 0.01, 0.5, 0.1, 0.01)
sigma = st.sidebar.slider("Sigma (Resources-Matter)", 0.01, 0.5, 0.1, 0.01)
kappa = st.sidebar.slider("Kappa (Resources-Entropy)", 0.01, 0.5, 0.1, 0.01)
lambda_ = st.sidebar.slider("Lambda (Entropy-Matter)", 0.01, 0.5, 0.1, 0.01)
mu = st.sidebar.slider("Mu (Entropy-Energy)", 0.01, 0.5, 0.1, 0.01)
nu = st.sidebar.slider("Nu (Entropy-Resources)", 0.01, 0.5, 0.1, 0.01)
nonlin = st.sidebar.slider("omega (Non linearity)", 0.01, 0.5, 0.1, 0.01)

# Initial conditions
st.sidebar.header("Initial Conditions")
E0 = st.sidebar.number_input("Initial Energy (E0)", 0.0, 100.0, 100.0, 0.1)
M0 = st.sidebar.number_input("Initial Matter (M0)", 0.0, 100.0, 10.0, 0.1)
R0 = st.sidebar.number_input("Initial Resources (R0)", 0.0, 100.0, 10.0, 0.1)
S0 = st.sidebar.number_input("Initial Entropy (S0)", 0.0, 10.0, 5.0, 0.1)

# Time span
st.sidebar.header("Time Settings")
start_time = st.sidebar.number_input("Start Time", 0, 100, 0)
end_time = st.sidebar.number_input("End Time", 0, 100, 100)
time_points = st.sidebar.number_input("Number of Time Points", 100, 1000, 500)

# Solve the system of equations
params = [alpha, beta, gamma, delta, eta, rho, sigma, kappa, lambda_, mu, nu,nonlin]
initial_conditions = [E0, M0, R0, S0]
time_span = (start_time, end_time)
time_points_array = np.linspace(time_span[0], time_span[1], time_points)

solution = solve_ivp(
    system_equations,
    time_span,
    initial_conditions,
    t_eval=time_points_array,
    args=(params,)
)



# Check and adjust dimensions
if solution.t.shape[0] != time_points_array.shape[0]:
    time_points_array = solution.t  # Use the actual time points from the solver

# Extract the results
E, M, R, S = solution.y

# Apply bounds after solving
E = np.clip(E, 0, 4 * E0)  # Energy cannot be negative or exceed 4x initial
M = np.clip(M, 0, 4 * M0)  # Matter cannot be negative or exceed 4x initial
R = np.clip(R, 0, 4 * R0)  # Resources cannot be negative or exceed 4x initial
S = np.clip(S, 0, 5 * S0)       # Entropy cannot be negative


# Calculate relative variations
E_rel = (E - E0) / E0 * 100 if E0 != 0 else np.zeros_like(E)
M_rel = (M - M0) / M0 * 100 if M0 != 0 else np.zeros_like(M)
R_rel = (R - R0) / R0 * 100 if R0 != 0 else np.zeros_like(R)
S_rel = (S - S0) / S0 * 100 if S0 != 0 else np.zeros_like(S)

# Plot the results
st.header("Simulation Results")
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(time_points_array, E_rel, label="Energy variation (E %)", linewidth=2)
ax.plot(time_points_array, M_rel, label="Matter variation (M %)", linewidth=2)
ax.plot(time_points_array, R_rel, label="Resources variation (R %)", linewidth=2)
ax.plot(time_points_array, S_rel, label="Entropy variation (S %)", linewidth=2)
ax.set_xlabel("Time", fontsize=14)
ax.set_ylabel("Values", fontsize=14)
ax.set_title("Evolution of Variables in the Decarbonation System", fontsize=16)
ax.legend(fontsize=12)
ax.grid()
st.pyplot(fig)

# Additional plots
st.header("Additional Relationships")
fig1, ax1 = plt.subplots(figsize=(6, 4))
ax1.plot(E_rel, S_rel, label="Entropy vs Energy", color="red")
ax1.set_xlabel("Energy variation (E %)")
ax1.set_ylabel("Entropy variation (S %)")
ax1.legend()
ax1.grid()
st.pyplot(fig1)

fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.plot(E_rel, M_rel, label="Matter vs Energy", color="blue")
ax2.set_xlabel("Energy variation (E %)")
ax2.set_ylabel("Matter variation (M %)")
ax2.legend()
ax2.grid()
st.pyplot(fig2)

fig3, ax3 = plt.subplots(figsize=(6, 4))
ax3.plot(E_rel, R_rel, label="Energy vs Resources", color="green")
ax3.set_xlabel("Energy variation (E %)")
ax3.set_ylabel("Resources variation (R %)")
ax3.legend()
ax3.grid()
st.pyplot(fig3)

fig4, ax4 = plt.subplots(figsize=(6, 4))
ax4.plot(S_rel, R_rel, label="Entropy vs Resources", color="purple")
ax4.set_xlabel("Entropy variation (S %)")
ax4.set_ylabel("Resources variation (R %)")
ax4.legend()
ax4.grid()
st.pyplot(fig4)


# Provide insights
st.header("Insights")
st.markdown(
    "Adjust the parameters on the left to observe how different strategies affect the dynamics of the decarbonation system."
)
