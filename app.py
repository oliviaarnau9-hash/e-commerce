import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Radar de Hiper-personalización E-commerce",
    page_icon="⚡",
    layout="wide"
)

# --- ESTILOS CSS PERSONALIZADOS (ESTÉTICA VERCEL / DARK MODE) ---
st.markdown("""
    <style>
    /* Fondo general oscuro */
    .stApp {
        background-color: #090d16;
        color: #f3f4f6;
    }
    
    /* Ocultar elementos predeterminados de Streamlit para que parezca una app web limpia */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Estilo de Tarjetas KPI / Contenedores */
    .card-metric {
        background-color: #111827;
        border: 1px solid #1f2937;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        margin-bottom: 15px;
    }
    
    /* Títulos principales */
    h1, h2, h3 {
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO PRINCIPAL ---
st.markdown("""
    <div style="padding: 20px 0;">
        <h1 style="font-size: 2.2rem; font-weight: 800; margin-bottom: 5px;">⚡ Radar de Hiper-personalización en E-commerce</h1>
        <p style="color: #9ca3af; font-size: 1.1rem;">Plataforma interactiva de monitoreo estratégico y análisis de tendencias en tiempo real.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    df = pd.read_csv("tendencias.csv")
    df.columns = df.columns.str.strip() # Limpia espacios en las columnas
    return df

try:
    df = load_data()
    
    # Detección inteligente de columnas según tu planilla
    col_horizonte = next((col for col in df.columns if 'horizonte' in col.lower()), df.columns[0])
    
    # --- PANEL LATERAL (FILTROS) ---
    st.sidebar.markdown("### 🎛️ Filtros del Radar")
    horizontes_disponibles = ["Todos"] + list(df[col_horizonte].dropna().unique())
    filtro_horizonte = st.sidebar.selectbox("Horizonte Temporal", horizontes_disponibles)
    
    if filtro_horizonte != "Todos":
        df_filtrado = df[df[col_horizonte] == filtro_horizonte]
    else:
        df_filtrado = df

    # --- TARJETAS DE MÉTRICAS (KPI CARDS - ESTILO VERCEL) ---
    total_tendencias = len(df_filtrado)
    corto_plazo = len(df_filtrado[df_filtrado[col_horizonte].astype(str).str.contains("Corto", case=False, na=False)])
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""
            <div class="card-metric">
                <p style="color: #9ca3af; font-size: 0.9rem; margin: 0;">Total Registros</p>
                <h3 style="color: #38bdf8; font-size: 1.8rem; margin: 5px 0 0 0;">{total_tendencias}</h3>
            </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
            <div class="card-metric">
                <p style="color: #9ca3af; font-size: 0.9rem; margin: 0;">Corto Plazo (0-1 año)</p>
                <h3 style="color: #34d399; font-size: 1.8rem; margin: 5px 0 0 0;">{corto_plazo}</h3>
            </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
            <div class="card-metric">
                <p style="color: #9ca3af; font-size: 0.9rem; margin: 0;">Estado del Sistema</p>
                <h3 style="color: #c084fc; font-size: 1.8rem; margin: 5px 0 0 0;">Conectado</h3>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- GRÁFICO DINÁMICO ADAPTADO AL MODO OSCURO ---
    st.subheader("📊 Distribución Visual")
    if col_horizonte in df.columns:
        fig = px.histogram(df_filtrado, x=col_horizonte, color=col_horizonte,
                           color_discrete_sequence=["#38bdf8", "#34d399", "#c084fc", "#f472b6"])
        fig.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font_color="#f3f4f6",
            margin=dict(t=20, b=20, l=20, r=20),
            legend=dict(font=dict(color="#f3f4f6"))
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --- TABLA DE DATOS ESTILIZADA ---
    st.subheader("📋 Base de Datos de Tendencias")
    st.dataframe(df_filtrado, use_container_width=True, height=450)

except Exception as e:
    st.error(f"Error al procesar la aplicación: {e}")
