import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Radar de Hiper-personalización E-commerce",
    page_icon="⚡",
    layout="wide"
)

# --- ESTILOS CSS CLAVADOS AL DISEÑO DE VERCEL ---
st.markdown("""
    <style>
    /* Reset y fondo principal tipo Vercel */
    .stApp {
        background-color: #000000;
        color: #ededed;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Tarjetas estilo Vercel (Borde sutil, fondo gris oscuro plano) */
    .vercel-card {
        background-color: #0a0a0a;
        border: 1px solid #222222;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
        transition: border-color 0.2s ease;
    }
    .vercel-card:hover {
        border-color: #444444;
    }

    /* Tipografía de títulos */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 600;
        letter-spacing: -0.025em;
    }

    /* Tablas prolijas y oscuras */
    dataframe, .stDataFrame {
        border: 1px solid #222222;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA LIMPIA ---
st.markdown("""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 1.8rem; font-weight: 600; margin-bottom: 8px;">⚡ Radar de Hiper-personalización en E-commerce</h1>
        <p style="color: #888888; font-size: 0.95rem;">Monitoreo estratégico y análisis de tendencias en tiempo real.</p>
    </div>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    df = pd.read_csv("tendencias.csv")
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
    
    col_horizonte = next((col for col in df.columns if 'horizonte' in col.lower()), df.columns[0])
    
    # --- FILTRO LATERAL MINIMALISTA ---
    st.sidebar.markdown("### Filtros")
    horizontes_disponibles = ["Todos"] + list(df[col_horizonte].dropna().unique())
    filtro_horizonte = st.sidebar.selectbox("Horizonte Temporal", horizontes_disponibles)
    
    if filtro_horizonte != "Todos":
        df_filtrado = df[df[col_horizonte] == filtro_horizonte]
    else:
        df_filtrado = df

    # --- TARJETAS DE MÉTRICAS (ESTILO UI VERCEL) ---
    total = len(df_filtrado)
    corto = len(df_filtrado[df_filtrado[col_horizonte].astype(str).str.contains("Corto", case=False, na=False)])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="vercel-card">
                <span style="color: #888888; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">Total Tendencias</span>
                <div style="font-size: 1.8rem; font-weight: 600; color: #ffffff; margin-top: 6px;">{total}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="vercel-card">
                <span style="color: #888888; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">Corto Plazo</span>
                <div style="font-size: 1.8rem; font-weight: 600; color: #ffffff; margin-top: 6px;">{corto}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class="vercel-card">
                <span style="color: #888888; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">Estado</span>
                <div style="font-size: 1.8rem; font-weight: 600; color: #34d399; margin-top: 6px;">● Activo</div>
            </div>
        """, unsafe_allow_html=True)

    # --- SECCIÓN DE DATOS (ESTILO CONTENEDOR VERCEL) ---
    st.markdown("""
        <div class="vercel-card" style="margin-top: 20px;">
            <h3 style="font-size: 1.1rem; margin-bottom: 15px;">Base de Datos de Tendencias</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(df_filtrado, use_container_width=True, height=450)

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
