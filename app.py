import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página con diseño ancho y limpio
st.set_page_config(
    page_title="Radar de Hiper-personalización E-commerce",
    page_icon="⚡",
    layout="wide"
)

# Estilos CSS personalizados para darle un toque moderno (tipo app web)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    h1 {
        color: #ffffff;
        font-weight: 700;
    }
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal
st.title("⚡ Radar de Hiper-personalización en E-commerce")
st.markdown("Panel interactivo de tendencias y análisis estratégico en tiempo real.")
st.markdown("---")

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    df = pd.read_csv("tendencias.csv")
    return df

try:
    df = load_data()
    
    # --- MÉTRICAS SUPERIORES (Estilo Tarjetas) ---
    col1, col2, col3, col4 = st.columns(4)
    
    total_tendencias = len(df)
    corto_plazo = len(df[df['Horizonte_Temporal'].str.contains("Corto", case=False, na=False)]) if 'Horizonte_Temporal' in df.columns else 0
    mediano_plazo = len(df[df['Horizonte_Temporal'].str.contains("Mediano", case=False, na=False)]) if 'Horizonte_Temporal' in df.columns else 0
    
    col1.metric("📊 Total Tendencias", total_tendencias)
    col2.metric("🚀 Corto Plazo (0-1 año)", corto_plazo)
    col3.metric("📈 Mediano Plazo", mediano_plazo)
    col4.metric("🌐 Estado", "Activo / En vivo")

    st.markdown("---")

    # --- SECCIÓN DE GRÁFICOS Y FILTROS ---
    col_izq, col_der = st.columns([1, 1])

    with col_izq:
        st.subheader("📌 Distribución por Horizonte")
        if 'Horizonte_Temporal' in df.columns:
            fig = px.pie(df, names="Horizonte_Temporal", hole=0.4,
                           color_discrete_sequence=px.colors.sequential.Tealgrn)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
            st.plotly_chart(fig, use_container_width=True)

    with col_der:
        st.subheader("🔍 Análisis Rápido de Brechas")
        if 'Brecha_Actual' in df.columns:
            fig2 = px.bar(df, x="ID_Tendencia", y="Brecha_Actual" if 'Brecha_Actual' in df.columns else None,
                          color="Horizonte_Temporal", title="Brechas Actuales por Tendencia")
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- TABLA DE DATOS ESTILIZADA ---
    st.subheader("📋 Base de Datos Completa de Tendencias")
    st.dataframe(df, use_container_width=True, height=400)

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
