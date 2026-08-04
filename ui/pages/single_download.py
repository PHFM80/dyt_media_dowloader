#ui\pages\single_download.py
import streamlit as st
from services.download_manager_service import DownloadManagerService
from services.project_manager_service import ProjectManagerService
from ui.components.video_info_card import render_video_info_card
from ui.components.download_controls import render_download_controls
from ui.components.donation_button import render_donation_button

def render_single_download():
    if st.button("← Volver al inicio", key="btn_back_single"):
        st.session_state.page = "Inicio"
        st.rerun()
    
    # Solo logo
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.image("assets/banners/TITULO_SUBTITULO_OSCURO.png", width=600)
    render_donation_button()
    st.markdown("---")
    st.header("📹 Descarga Única")
    st.markdown("Ingresa la URL del video que deseas descargar")
    
    project_name = st.text_input(
        "Nombre del proyecto (opcional)", 
        value=st.session_state.get("single_project_name", ""),
        placeholder="Ej: Mi_Video_Favorito"
    )
    st.session_state.single_project_name = project_name
    
    url = st.text_input("URL del video", placeholder="https://www.youtube.com/watch?v=...")
    
    if st.button("Obtener información", type="primary", width="stretch"):
        if not url:
            st.warning("Por favor ingresa una URL")
            return
        
        with st.spinner("Obteniendo información del video..."):
            try:
                service = DownloadManagerService()
                info = service.get_video_info(url)
                st.session_state.video_info = info
                st.session_state.current_url = url
                st.success("✅ Información obtenida correctamente")
            except Exception as e:
                st.error(f"Error al obtener información: {str(e)}")
    
    if "video_info" in st.session_state:
        st.markdown("---")
        render_video_info_card(st.session_state.video_info)
        render_download_controls(st.session_state.video_info, st.session_state.get("current_url"))