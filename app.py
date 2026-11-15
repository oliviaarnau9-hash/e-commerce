import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Radar de Hiper-personalización E-commerce",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Radar de Hiper-personalización en E-commerce")
st.markdown("Dashboard dinámico interactivo.")

# --- CARGA DEL ARCHIVO LOCAL ---
@st.cache_data
def load_data():
    # Buscamos el archivo CSV subido al repositorio
    # Reemplaza 'tendencias.csv' con el nombre exacto del archivo que descargues, o sube tu CSV a GitHub
    df = pd.read_csv("tendencias.csv")
    return df

try:
    df = load_data()
    
    # Métricas superiores
    col1, col2, col3 = st.columns(3)
    total_tendencias = len(df)
    corto_plazo = len(df[df['Horizonte_Temporal'].str.contains("Corto", case=False, na=False)]) if 'Horizonte_Temporal' in df.columns else 0
    
    col1.metric("Tendencias Totales", total_tendencias)
    col2.metric("Horizonte Corto (0-1 año)", corto_plazo)
    col3.metric("Fuentes Analizadas", "Varios reportes")

    st.markdown("---")

    # Gráfico de barras interactivo
    st.subheader("Distribución por Horizonte Temporal")
    if 'Horizonte_Temporal' in df.columns:
        fig = px.histogram(df, x="Horizonte_Temporal", color="Horizonte_Temporal", 
                           title="Tendencias según Horizonte")
        st.plotly_chart(fig, use_container_width=True)

    # Tabla de datos detallada
    st.subheader("Base de Datos de Tendencias")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.warning("Sube un archivo llamado 'tendencias.csv' a tu repositorio de GitHub para ver los datos.")
