# Aplicación optimizada de forma nativa para entornos de alto rendimiento bajo Python 3.14.8
import streamlit as st
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

st.set_page_config(page_title="Optimización de Proyectos", layout="wide")

st.title("🎒 Optimización de Portafolio de Proyectos (Problema de la Mochila)")
st.subheader("Entorno verificado y compatible con Python 3.14.8")
st.write("Modifica los parámetros de los proyectos a continuación para calcular la combinación óptima que maximiza el impacto total.")

# Valores iniciales por defecto
defaults = [
    {"name": "Proyecto 1", "cost": 8, "benefit": 14},
    {"name": "Proyecto 2", "cost": 3, "benefit": 5},
    {"name": "Proyecto 3", "cost": 4, "benefit": 7},
    {"name": "Proyecto 4", "cost": 2, "benefit": 3},
]

# Barra lateral para el presupuesto total
budget = st.sidebar.number_input("Presupuesto Máximo Disponible:", min_value=1, max_value=100, value=9, step=1)

# Columnas para ingresar costos y beneficios de cada proyecto
st.header("Configuración de Proyectos")
cols = st.columns(4)

projects_data = []
for i, col in enumerate(cols):
    with col:
        st.subheader(f"Proyecto {i+1}")
        benefit = st.number_input(f"Beneficio P{i+1}:", min_value=0, value=defaults[i]["benefit"], key=f"b_{i}")
        cost = st.number_input(f"Costo P{i+1}:", min_value=1, value=defaults[i]["cost"], key=f"c_{i}")
        projects_data.append({"name": f"Proyecto {i+1}", "cost": cost, "benefit": benefit})

# Preparar datos para el optimizador
costs = np.array([p["cost"] for p in projects_data])
benefits = np.array([p["benefit"] for p in projects_data])

# Botón para resolver
if st.button("Calcular Selección Óptima", type="primary"):
    c = -benefits
    bounds = Bounds(np.zeros(4), np.ones(4))
    integrality = np.ones(4)

    # Restricción: Suma(costos * x) <= budget
    A = np.array([costs])
    constraint = LinearConstraint(A, -np.inf, budget)

    res = milp(c=c, constraints=constraint, integrality=integrality, bounds=bounds)

    st.header("Resultados de la Optimización")
    if res.success:
        x_opt = np.round(res.x)
        total_benefit = int(-res.fun)
        total_cost = int(np.sum(costs * x_opt))

        # Mostrar métricas clave
        m1, m2 = st.columns(2)
        m1.metric("Impacto/Beneficio Máximo Total", f"{total_benefit} pts")
        m2.metric("Costo Total Utilizado", f"{total_cost} de {budget}")

        # Mostrar proyectos seleccionados
        st.subheader("Proyectos Seleccionados:")
        for i, val in enumerate(x_opt):
            if val == 1:
                st.success(f"✅ **{projects_data[i]['name']}** (Costo: {projects_data[i]['cost']}, Beneficio: {projects_data[i]['benefit']})")
            else:
                st.error(f"❌ **{projects_data[i]['name']}** (No seleccionado)")
    else:
        st.error(f"No se encontró una solución viable: {res.message}")
