import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(layout="wide")
st.title("Deco - Dashboard de Apuestas")

# Simulación de partidos del día
partidos = [
    {"Partido": "Boca vs Independiente", "FechaHora": "Lunes 20/05 - 21:30"},
    {"Partido": "River vs Racing", "FechaHora": "Lunes 20/05 - 23:00"}
]

modelos = ["Clásico", "Value Bets", "Alta Precisión", "Combinadas", "Subestimados", "Live Bot"]
tipos_apuesta = ["Más de 2.5 goles", "Ambos anotan", "Doble oportunidad", "Menos de 3.5", "Empate al descanso"]

# Simular apuestas
data_apuestas = []
for partido in partidos:
    for modelo in modelos:
        for i in range(random.randint(2, 4)):
            tipo = random.choice(tipos_apuesta)
            cuota = round(random.uniform(1.8, 2.5), 2)
            ganada = random.choice([True, False])
            ganancia = round(1000 * cuota) if ganada else -1000
            data_apuestas.append({
                "Modelo": modelo,
                "Partido": partido["Partido"],
                "Fecha y Hora": partido["FechaHora"],
                "Tipo de Apuesta": tipo,
                "Cuota": cuota,
                "Resultado": "✅" if ganada else "❌",
                "Ganancia ($)": ganancia
            })

df = pd.DataFrame(data_apuestas)

# Mostrar tabla general
st.subheader("Apuestas del Día")
st.dataframe(df, use_container_width=True)

# Mostrar detalle por modelo
st.subheader("Ver Detalle por Modelo")
for modelo in df["Modelo"].unique():
    with st.expander(f"Ver detalle: {modelo}"):
        st.dataframe(df[df["Modelo"] == modelo], use_container_width=True)

# Resumen por modelo
st.subheader("Resumen por Modelo")
resumen = df.groupby("Modelo").agg(
    Apuestas=("Tipo de Apuesta", "count"),
    Aciertos=("Resultado", lambda x: sum(x == "✅")),
    GananciaTotal=("Ganancia ($)", "sum")
).reset_index()
resumen["Rentabilidad (%)"] = resumen["GananciaTotal"] / (resumen["Apuestas"] * 1000) * 100
st.dataframe(resumen.style.format({"GananciaTotal": "${:,.0f}", "Rentabilidad (%)": "{:.2f}%"}))

# Resumen general del día
st.subheader("Resumen General del Día")
total_apuestas = resumen["Apuestas"].sum()
total_ganancia = resumen["GananciaTotal"].sum()
rentabilidad_total = total_ganancia / (total_apuestas * 1000) * 100
icono = "🟢" if total_ganancia >= 0 else "🔴"
st.markdown(f"**{icono} Total Apuestas:** {total_apuestas} | **Ganancia Total:** ${total_ganancia:,.0f} | **Rentabilidad:** {rentabilidad_total:.2f}%")
