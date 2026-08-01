#ui\components\download_controls.py
import streamlit as st
from services.download_manager_service import DownloadManagerService
from services.project_manager_service import ProjectManagerService


def render_download_controls(info: dict, url: str):
    st.markdown("---")
    st.subheader("Opciones de descarga")
    
    col1, col2 = st.columns(2)
    
    with col1:
        download_type = st.radio(
            "Tipo de descarga",
            ["Video", "Audio (MP3)"],
            horizontal=True
        )
    
    with col2:
        if download_type == "Video":
            quality = st.selectbox("Calidad de video", info["video_formats"])
        else:
            quality = st.selectbox("Calidad de audio", info["audio_formats"])
    
    if st.button("Descargar", type="primary", width="stretch"):
        if not url:
            st.error("URL no disponible")
            return
        
        with st.spinner("Preparando descarga..."):
            try:
                project_name = st.session_state.get("single_project_name", "") or "Descarga_Unica"
                project_manager = ProjectManagerService()
                project = project_manager.create_project(name=project_name, is_single_session=True)
                
                download_manager = DownloadManagerService()
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def progress_callback(progress_data):
                    if progress_data['status'] == 'downloading':
                        percent_str = progress_data.get('percent', '0%').strip('%')
                        try:
                            percent = float(percent_str)
                            progress_bar.progress(percent / 100)
                        except:
                            pass
                        status_text.text(f"Descargando... {progress_data.get('percent', '0%')} - {progress_data.get('speed', 'N/A')}")
                    elif progress_data['status'] == 'finished':
                        progress_bar.progress(1.0)
                        status_text.text("Descarga completada")
                
                if download_type == "Video":
                    quality_value = quality.split("p")[0] if "p" in quality else "best"
                    task = download_manager.download_video(url, quality_value, project, progress_callback)
                else:
                    quality_value = quality.split()[0] if "kbps" in quality else "320"
                    task = download_manager.download_audio(url, quality_value, project, progress_callback)
                
                st.success(f"✅ Descarga completada: `{task.file_path}`")
                project_manager.clear_current_project()
                
            except Exception as e:
                st.error(f"Error en la descarga: {str(e)}")