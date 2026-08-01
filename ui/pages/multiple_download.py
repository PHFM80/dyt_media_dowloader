#ui\pages\multiple_download.py
import streamlit as st
import tempfile
import os
from services.download_manager_service import DownloadManagerService
from services.project_manager_service import ProjectManagerService
from services.url_cleaner_service import URLCleanerService
from services.file_reader_service import FileReaderService


def render_multiple_download():
    if st.button("← Volver al inicio"):
        st.session_state.page = "Inicio"
        st.rerun()
    
    st.header("📋 Descarga Múltiple")
    
    project_name = st.text_input(
        "Nombre del proyecto", 
        value=st.session_state.get("multi_project_name", "Proyecto_Multiple"),
        help="Todas las descargas se guardarán en una carpeta con este nombre en tu carpeta de Descargas."
    )
    st.session_state.multi_project_name = project_name

    tab1, tab2 = st.tabs(["Pegar URLs", "Cargar archivo"])
    
    with tab1:
        urls_text = st.text_area("Pega las URLs aquí (una por línea)", height=150)
        if st.button("Procesar URLs", type="primary"):
            if not urls_text:
                st.warning("Por favor ingresa al menos una URL")
                return
            
            with st.spinner("Limpiando y validando URLs..."):
                raw_urls = [line.strip() for line in urls_text.split('\n') if line.strip()]
                cleaned_urls = URLCleanerService.clean_urls(raw_urls)
                
            if not cleaned_urls:
                st.error("No se encontraron URLs válidas.")
                return
            
            _fetch_multiple_info(cleaned_urls)

    with tab2:
        uploaded_file = st.file_uploader("Selecciona un archivo (TXT o DOCX)", type=['txt', 'docx'])
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            
            try:
                with st.spinner("Leyendo archivo..."):
                    urls = FileReaderService.read_file(tmp_path)
                    if not urls:
                        st.error("No se encontraron URLs en el archivo.")
                    else:
                        _fetch_multiple_info(urls)
            finally:
                os.unlink(tmp_path)

    if "multiple_info_list" in st.session_state and st.session_state.multiple_info_list:
        st.markdown("---")
        st.subheader(f"Videos encontrados ({len(st.session_state.multiple_info_list)})")
        
        with st.container(height=400):
            for info in st.session_state.multiple_info_list:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(info.get('thumbnail', ''), width=120)
                with col2:
                    st.markdown(f"**{info.get('title', 'Sin título')}**")
                    st.markdown(f"Canal: {info.get('uploader', 'Desconocido')} | Duración: {info.get('duration', 'N/A')}s")
                st.divider()
        
        st.markdown("---")
        st.subheader("Acciones de descarga")
        st.markdown("Configura el formato y calidad para descargar TODOS los videos de la lista.")
        
        col1, col2, col3 = st.columns([1, 1, 1.2])
        with col1:
            batch_type = st.radio("Tipo", ["Video", "Audio (MP3)"], horizontal=True, key="batch_type")
        
        with col2:
            if batch_type == "Video":
                batch_quality = st.selectbox("Calidad", ["best", "1080", "720", "480"], index=0, key="batch_q_vid")
            else:
                batch_quality = st.selectbox("Calidad", ["320", "192", "128", "best"], index=0, key="batch_q_aud")
                
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Iniciar Descarga Masiva", type="primary", width="stretch"):
                _execute_batch_download(batch_type, batch_quality)


def _fetch_multiple_info(urls: list):
    st.session_state.multiple_urls = urls
    st.session_state.multiple_info_list = []
    
    with st.spinner(f"Obteniendo información de {len(urls)} videos..."):
        progress_bar = st.progress(0)
        service = DownloadManagerService()
        for i, url in enumerate(urls):
            try:
                info = service.get_video_info(url)
                info['_url'] = url
                st.session_state.multiple_info_list.append(info)
            except Exception as e:
                st.warning(f"Error al obtener info de {url}: {str(e)}")
            progress_bar.progress((i + 1) / len(urls))
    
    st.success(f"✅ {len(st.session_state.multiple_info_list)} videos listos para descargar.")


def _execute_batch_download(download_type: str, quality: str):
    urls = [info['_url'] for info in st.session_state.multiple_info_list]
    project_name = st.session_state.get("multi_project_name", "Proyecto_Multiple")
    
    with st.spinner(f"Preparando proyecto '{project_name}'..."):
        project_manager = ProjectManagerService()
        project = project_manager.create_project(name=project_name, is_single_session=False)
        
        download_manager = DownloadManagerService()
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        completed = 0
        total = len(urls)
        
        for i, url in enumerate(urls):
            status_text.text(f"Procesando {i+1}/{total}... (Se reintentará automáticamente si falla)")
            try:
                if download_type == "video":
                    task = download_manager.download_video(url, quality, project)
                else:
                    task = download_manager.download_audio(url, quality, project)
                
                if task.status == "completed":
                    completed += 1
                else:
                    st.warning(f"⚠️ Falló {url}: {task.error_message}")
            except Exception as e:
                st.error(f"Error crítico en {url}: {str(e)}")
                
            progress_bar.progress((i + 1) / total)
        
        status_text.text("¡Proceso finalizado!")
        st.success(f"✅ Descarga completada: {completed}/{total} archivos guardados en: `{project.base_path}`")
        
        if st.button("Nueva descarga múltiple"):
            st.session_state.pop("multiple_info_list", None)
            st.session_state.pop("multiple_urls", None)
            st.rerun()