import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# Titre principal
st.title("Exploration des Dérivées Partielles")
st.markdown("Plongez dans le concept des dérivées partielles avec des visualisations 3D interactives, des exercices pratiques et des quiz pédagogiques.
")

# **1. Définition et Concepts de Dérivées Partielles**
st.header("1. Définition et Concepts")
st.markdown("""
Les dérivées partielles permettent d'étudier comment une grandeur varie par rapport à une variable tout en maintenant les autres constantes.

- **Variation de température avec la profondeur :** ∂T/∂z
- **Variation de pression selon la distance :** ∂P/∂x
""")

# **2. Visualisation Interactive : Variation de T(x, y, z)**
st.header("2. Visualisation Interactive")
st.markdown("""
### Exemple : Température T(x, y, z) = sin(x) * cos(y) * exp(-z)

Ce graphique montre comment T varie dans un espace 3D en fonction des variables x, y, et z.
""")

# Variables pour la simulation
x_vals = np.linspace(0, 2 * np.pi, 50)
y_vals = np.linspace(0, 2 * np.pi, 50)
x_grid, y_grid = np.meshgrid(x_vals, y_vals)
z_slider = st.slider("Choisissez la valeur de z :", 0.1, 2.0, 0.5, step=0.1)

# Calcul de T
T_func = lambda x, y, z: np.sin(x) * np.cos(y) * np.exp(-z)
T_vals = T_func(x_grid, y_grid, z_slider)

# Graphique 3D
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x_grid, y_grid, T_vals, cmap='viridis')
ax.set_title("Variation de T(x, y, z)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("T")
st.pyplot(fig)

# **3. Exercices Guidés**
st.header("3. Exercices Guidés")
st.markdown("""
### Exercice 1 : Calcul de ∂T/∂z pour T(x, y, z) = 10x² + 5y - 2z
""")
x, y, z = sp.symbols("x y z")
T_expr = 10 * x**2 + 5 * y - 2 * z
partial_derivative_z = sp.diff(T_expr, z)

st.write(f"**La dérivée partielle de T par rapport à z est :** {partial_derivative_z}")

# Input pour l'utilisateur
x_input = st.number_input("Entrez une valeur pour x :", value=1.0, step=0.1)
y_input = st.number_input("Entrez une valeur pour y :", value=2.0, step=0.1)
z_input = st.number_input("Entrez une valeur pour z :", value=0.5, step=0.1)

T_value = T_expr.subs({x: x_input, y: y_input, z: z_input})
partial_z_value = partial_derivative_z.subs({z: z_input})

st.write(f"**À x = {x_input}, y = {y_input}, z = {z_input} :**")
st.write(f"Valeur de T : {T_value}")
st.write(f"Dérivée partielle ∂T/∂z : {partial_z_value}")

# **4. Quiz interactif**
st.header("4. Quiz Interactif")
st.markdown("""
Testez votre compréhension des concepts de dérivées partielles avec des questions interactives.
""")

# Question 1
st.subheader("Question 1 :")
question_1 = st.radio(
    "Si ∂T/∂z est négative, cela signifie que :",
    ("T augmente avec z", "T diminue avec z", "T reste constante"),
)
if st.button("Vérifier la réponse - Question 1"):
    if question_1 == "T diminue avec z":
        st.success("Correct ! Une dérivée partielle négative indique une diminution.")
    else:
        st.error("Incorrect. Réessayez.")

# Question 2
st.subheader("Question 2 :")
question_2 = st.radio(
    "Quelle est la dérivée partielle de T(x, y, z) = x² + y² + z² par rapport à x ?",
    ("2x", "2y", "2z"),
)
if st.button("Vérifier la réponse - Question 2"):
    if question_2 == "2x":
        st.success("Correct ! La dérivée partielle de x² est 2x.")
    else:
        st.error("Incorrect. Réessayez.")

# **5. Téléchargement des Résultats**
st.header("5. Téléchargement des Résultats")
st.markdown("Téléchargez les résultats de vos calculs et exercices.")

data = {
    "Exercice": ["Exercice 1", "Quiz Question 1", "Quiz Question 2"],
    "Résultat": [
        f"T = {T_value}, ∂T/∂z = {partial_z_value}",
        "Correct" if question_1 == "T diminue avec z" else "Incorrect",
        "Correct" if question_2 == "2x" else "Incorrect",
    ],
}
df = pd.DataFrame(data)
csv = df.to_csv(index=False)

st.download_button(
    label="Télécharger les résultats",
    data=csv,
    file_name="resultats_derivées_partielles.csv",
    mime="text/csv",
)

# **6. Résumé**
st.header("6. Résumé")
st.markdown("""
- **Dérivées Partielles** mesurent comment une grandeur varie par rapport à une variable en fixant les autres.
- **Visualisation 3D** permet de comprendre intuitivement ces concepts.
- **Exercices et Quiz** renforcent la compréhension.
""")
