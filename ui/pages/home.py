#ui\pages\home.py
import streamlit as st

def render_home():
    st.title("🎬 Descargar YouTube")
    st.markdown("---")
    
    st.markdown("""
    ### Bienvenido a tu herramienta de descargas
    
    Esta aplicación te permite descargar contenido de YouTube de forma simple y rápida.
    
    **Características principales:**
    - 📹 Descarga videos en máxima calidad
    - 🎵 Extrae audio en formato MP3
    - 📋 Descarga individual o múltiple
    - 📁 Organización automática de archivos
    
    Selecciona una opción para comenzar:
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📹 Descarga Única")
        st.markdown("Descarga un solo video o audio desde una URL")
        if st.button("Comenzar descarga única", type="primary", width="stretch"):
            st.session_state.page = "Descarga Única"
            st.rerun()
    
    with col2:
        st.markdown("### 📋 Descarga Múltiple")
        st.markdown("Descarga varios videos pegando URLs o cargando un archivo")
        if st.button("Comenzar descarga múltiple", type="primary", width="stretch"):
            st.session_state.page = "Descarga Múltiple"
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    <small>Powered by yt-dlp | Interfaz moderna con Streamlit</small>
    </div>
    """, unsafe_allow_html=True)