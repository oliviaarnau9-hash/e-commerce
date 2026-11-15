import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Radar de Hiper-personalización E-commerce",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Radar de Hiper-personalización en E-commerce")
st.markdown("Plataforma interactiva de monitoreo estratégico y análisis de tendencias en tiempo real.")
st.markdown("---")

# --- CARGA DE DATOS FLEXIBLE ---
@st.cache_data
def load_data():
    df = pd.read_csv("tendencias.csv")
    df.columns = df.columns.str.strip() # Limpia espacios en los títulos
    return df

try:
    df = load_data()
    
    # --- PANEL LATERAL DE FILTROS ---
    st.sidebar.header("Panel de Filtros")
    
    # Buscamos la columna de horizonte de manera inteligente
    col_horizonte = next((col for col in df.columns if 'horizonte' in col.lower()), df.columns[0])
    
    horizontes_disponibles = ["Todos"] + list(df[col_horizonte].dropna().unique())
    filtro_horizonte = st.sidebar.selectbox("Filtrar por Horizonte Temporal", horizontes_disponibles)
    
    if filtro_horizonte != "Todos":
        df_filtrado = df[df[col_horizonte] == filtro_horizonte]
    else:
        df_filtrado = df

    # --- MÉTRICAS SUPERIORES ---
    col1, col2, col3, col4 = st.columns(4)
    total_registros = len(df_filtrado)
    
    col1.metric("📊 Total Registros", total_registros)
    col2.metric("🌐 Estado", "Conectado")
    col3.metric("🚀 Base", "CSV Local")
    col4.metric("⚡ Visual", "Activo")

    st.markdown("---")

    # --- GRÁFICO ESTILIZADO ---
    st.subheader("Distribución por Horizonte Temporal")
    if col_horizonte in df.columns:
        fig = px.histogram(df_filtrado, x=col_horizonte, color=col_horizonte,
                           color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    # --- TABLA DE DATOS ---
    st.subheader("📋 Estructura de la Base de Datos")
    st.dataframe(df_filtrado, use_container_width=True, height=400)

except Exception as e:
    st.error(f"Error al procesar el archivo: {e}")
