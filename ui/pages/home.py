#ui\pages\home.py
import streamlit as st
from ui.components.donation_button import render_donation_button


def render_home():
    # Solo banner/título
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.image("assets/banners/TITULO_SUBTITULO_OSCURO.png", width=600)
    
    st.markdown("---")
    
    st.markdown("""
    ### Bienvenido a tu herramienta de descargas
    
    Esta aplicación te permite descargar contenido de YouTube de forma simple y rápida.
    
    **Características principales:**
    - 📹 Descarga videos en máxima calidad
    - 🎵 Extrae audio en formato MP3
    - 📋 Descarga individual o múltiple
    - 📁 Organización automática de archivos
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
    
    st.markdown("### 🔗 Conectá con nosotros")
    col_fb, col_ig = st.columns(2)
    with col_fb:
        st.markdown("🔵 [Facebook - DYT Digitaliza](https://www.facebook.com/profile.php?id=61571476868202)")
    with col_ig:
        st.markdown("🟣 [Instagram - @dytdigitaliza](https://www.instagram.com/dytdigitaliza/)")
    
    render_donation_button()
    
    st.markdown("---")
    
    # Footer con branding
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        col_text, col_logo = st.columns([1, 1])
        with col_text:
            st.markdown(
                "<div style='text-align: right; color: gray; padding-top: 10px;'>"
                "<small>Powered by <strong>D&T-Digitaliza</strong></small>"
                "</div>",
                unsafe_allow_html=True
            )
        with col_logo:
            st.image("assets/logos/LOGO_DYT.png", width=40)