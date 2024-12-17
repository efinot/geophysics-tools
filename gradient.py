import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Liste des fonctions disponibles
FUNCTIONS = {
    "Polynomiale : ax^b + cy^d": lambda x, y, a, b, c, d: a * x**b + c * y**d,
    "Exponentielle : ae^(bx) + ce^(dy)": lambda x, y, a, b, c, d: a * np.exp(b * x) + c * np.exp(d * y),
    "Sinusoïdale : a*sin(bx) + c*cos(dy)": lambda x, y, a, b, c, d: a * np.sin(b * x) + c * np.cos(d * y),
    "Logarithmique : a*log(bx) + c*log(dy)": lambda x, y, a, b, c, d: a * np.log(np.abs(b * x) + 1) + c * np.log(np.abs(d * y) + 1),
    "Tangente : a*tan(bx) + c*tan(dy)": lambda x, y, a, b, c, d: a * np.tan(b * x) + c * np.tan(d * y),
}

# Gradient de la fonction (approximatif par dérivation numérique)
def grad_f(f, x, y, a, b, c, d):
    h = 1e-5  # Petits pas pour l'approximation
    df_dx = (f(x + h, y, a, b, c, d) - f(x - h, y, a, b, c, d)) / (2 * h)
    df_dy = (f(x, y + h, a, b, c, d) - f(x, y - h, a, b, c, d)) / (2 * h)
    return df_dx, df_dy

# Interface utilisateur Streamlit
st.title("Visualisation Interactive du Gradient")
st.write("Explorez différentes fonctions et observez comment le gradient varie.")

# Sélection de la fonction
function_name = st.selectbox("Choisissez une fonction :", list(FUNCTIONS.keys()))
selected_function = FUNCTIONS[function_name]

# Paramètres interactifs
a = st.slider("Coefficient a", 0.1, 5.0, 1.0, 0.1)
b = st.slider("Paramètre b", 1.0, 4.0, 2.0, 0.5)
c = st.slider("Coefficient c", 0.1, 5.0, 1.0, 0.1)
d = st.slider("Paramètre d", 1.0, 4.0, 2.0, 0.5)

# Définir l'espace des variables
x = np.linspace(-5, 5, 30)
y = np.linspace(-5, 5, 30)
X, Y = np.meshgrid(x, y)

# Calculer les valeurs de la fonction et du gradient
Z = selected_function(X, Y, a, b, c, d)
U, V = grad_f(selected_function, X, Y, a, b, c, d)

# Affichage
fig, ax = plt.subplots(figsize=(8, 6))

# Courbes de niveau
contour = ax.contour(X, Y, Z, levels=20, cmap='coolwarm')
ax.clabel(contour, inline=True, fontsize=8)

# Vecteurs du gradient
ax.quiver(X, Y, U, V, color="black", alpha=0.7)

# Titres et labels
ax.set_title(f"Gradient de la fonction : {function_name}")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(alpha=0.5)

st.pyplot(fig)

