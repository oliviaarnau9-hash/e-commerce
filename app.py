import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial de la página con diseño ancho y tema oscuro moderno
st.set_page_config(
    page_title="Radar de Hiper-personalización E-commerce",
    page_icon="⚡",
    layout="wide"
)

# Estilos CSS personalizados para imitar exactamente la estética oscura, limpia y profesional de tu Vercel
st.markdown("""
    <style>
    /* Estilos globales y tipografía */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    
    /* Encabezados principales */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }

    /* Tarjetas de métricas personalizadas */
    .metric-container {
        background-color: #111827;
        border: 1px solid #1f2937;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-title {
        font-size: 14px;
        color: #9ca3af;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 28px;
        color: #38bdf8;
        font-weight: 700;
        margin-top: 5px;
    }

    /* Contenedores de gráficos y tablas */
    div.stPlotlyChart {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Ajustes generales de tablas y selectores */
    .stDataFrame {
        border-radius: 12px;
        border: 1px solid #1f2937;
    }
    </style>
""", unsafe_allow_html=True)

# Título y Descripción de la App
st.title("⚡ Radar de Hiper-personalización en E-commerce")
st.markdown("<p style='color: #9ca3af; font-size: 16px;'>Plataforma interactiva de monitoreo estratégico, análisis de brechas y tendencias emergentes alimentada en tiempo real.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- CARGA DE DATOS DESDE 'tendencias.csv' ---
@st.cache_data
def load_data():
    # Lee el archivo CSV local cargado en el repositorio de GitHub
    df = pd.read_csv("tendencias.csv")
    return df

try:
    df = load_data()
    
    # --- FILTROS SUPERIORES DE INTERACTIVIDAD ---
    st.sidebar.header("🔍 Panel de Filtros")
    
    # Filtro por Horizonte Temporal si existe la columna
    horizontes = ["Todos"]
    if 'Horizonte_Temporal' in df.columns:
        horizontes += list(df['Horizonte_Temporal'].dropna().unique())
    
    filtro_horizonte = st.sidebar.selectbox("Filtrar por Horizonte Temporal", horizontes)
    
    # Aplicar filtro si el usuario selecciona uno específico
    df_filtered = df.copy()
    if filtro_horizonte != "Todos":
        df_filtered = df_filtered[df_filtered['Horizonte_Temporal'] == filtro_horizonte]

    # --- MÉTRICAS SUPERIORES (KPI Cards) ---
    col1, col2, col3, col4 = st.columns(4)
    
    total_tendencias = len(df_filtered)
    corto_plazo = len(df[df['Horizonte_Temporal'].astype(str).str.contains("Corto", case=False, na=False)])
    mediano_plazo = len(df[df['Horizonte_Temporal'].astype(str).str.contains("Mediano", case=False, na=False)])
    
    with col1:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Tendencias Totales</div>
                <div class="metric-value">{total_tendencias}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Corto Plazo (0-1 año)</div>
                <div class="metric-value" style="color: #34d399;">{corto_plazo}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Mediano Plazo (1-3 años)</div>
                <div class="metric-value" style="color: #f472b6;">{mediano_plazo}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Estado de Base</div>
                <div class="metric-value" style="color: #60a5fa;">Sincronizado</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SECCIÓN DE GRÁFICOS INTERACTIVOS (Plotly con estética oscura Vercel) ---
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("📊 Distribución por Horizonte Temporal")
        if 'Horizonte_Temporal' in df_filtered.columns and not df_filtered.empty:
            fig_pie = px.pie(
                df_filtered, 
                names="Horizonte_Temporal", 
                hole=0.5,
                color_discrete_sequence=['#38bdf8', '#34d399', '#f472b6', '#fbbf24']
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)", 
                font_color="#f3f4f6",
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No hay datos suficientes para mostrar el gráfico de horizontes.")

    with col_der:
        st.subheader("📈 Tendencias por ID y Categoría")
        if 'ID_Tendencia' in df_filtered.columns and not df_filtered.empty:
            fig_bar = px.bar(
                df_filtered, 
                x="ID_Tendencia", 
                y=df_filtered.index,
                color="Horizonte_Temporal" if 'Horizonte_Temporal' in df_filtered.columns else None,
                color_discrete_sequence=['#38bdf8', '#34d399', '#f472b6']
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)", 
                font_color="#f3f4f6",
                xaxis_title="ID de Tendencia",
                yaxis_title="Volumen / Registro",
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No hay datos suficientes para mostrar el gráfico de barras.")

    st.markdown("---")

    # --- TABLA DE DATOS DETALLADA ESTILIZADA ---
    st.subheader("📋 Matriz Completa de Tendencias de Hiper-personalización")
    st.markdown("<p style='color: #9ca3af; font-size: 14px;'>Visualización detallada de las descripciones, brechas actuales y fuentes oficiales extraídas.</p>", unsafe_allow_html=True)
    
    # Mostrar el DataFrame interactivo optimizado
    st.dataframe(
        df_filtered, 
        use_container_width=True, 
        height=450
    )

except Exception as e:
    st.error(f"Error al procesar los datos de 'tendencias.csv': {e}")
    st.info("Asegúrate de que el archivo 'tendencias.csv' esté subido correctamente en la raíz de tu repositorio de GitHub.")
