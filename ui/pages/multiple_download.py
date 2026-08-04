#ui\pages\multiple_download.py
import streamlit as st
import tempfile
import os
from services.download_manager_service import DownloadManagerService
from services.project_manager_service import ProjectManagerService
from services.url_cleaner_service import URLCleanerService
from services.file_reader_service import FileReaderService
from services.playlist_service import PlaylistService
from ui.components.parallel_progress import render_parallel_progress
from utils.text_utils import clean_error_message
from ui.components.donation_button import render_donation_button

def render_multiple_download():
    if st.button("← Volver al inicio", key="btn_back_multi"):
        st.session_state.page = "Inicio"
        st.rerun()
    
    # Solo logo
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.image("assets/banners/TITULO_SUBTITULO_OSCURO.png", width=600)
    render_donation_button()
    
    st.markdown("---")
    st.header("📋 Descarga Múltiple")
    
    project_name = st.text_input(
        "Nombre del proyecto",
        value=st.session_state.get("multi_project_name", "Proyecto_Multiple"),
        help="Todas las descargas se guardarán en una carpeta con este nombre."
    )
    st.session_state.multi_project_name = project_name

    tab1, tab2 = st.tabs(["Pegar URLs", "Cargar archivo"])
    
    with tab1:
        urls_text = st.text_area("Pega las URLs aquí (una por línea)", height=150, key="urls_text_area")
        if st.button("Procesar URLs", type="primary", key="btn_process_urls", disabled=st.session_state.get("is_processing", False)):
            if not urls_text.strip():
                st.warning("Por favor ingresa al menos una URL")
            else:
                st.session_state.is_processing = True
                st.session_state.urls_to_process = urls_text
                st.rerun()
                
    if st.session_state.get("is_processing") and st.session_state.get("urls_to_process"):
        with st.status("Limpiando y validando URLs...", expanded=True):
            raw_urls = [line.strip() for line in st.session_state.urls_to_process.split('\n') if line.strip()]
            cleaned_urls = URLCleanerService.clean_urls(raw_urls)
            
        if not cleaned_urls:
            st.error("No se encontraron URLs válidas.")
            st.session_state.is_processing = False
            st.session_state.urls_to_process = ""
            st.rerun()
        else:
            _process_urls(cleaned_urls)
            st.session_state.is_processing = False
            st.session_state.urls_to_process = ""
            st.rerun()

    with tab2:
        uploaded_file = st.file_uploader("Selecciona un archivo (TXT o DOCX)", type=['txt', 'docx'], key="file_uploader_multi")
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            
            try:
                with st.status("Leyendo archivo...", expanded=True):
                    urls = FileReaderService.read_file(tmp_path)
                    if not urls:
                        st.error("No se encontraron URLs en el archivo.")
                    else:
                        _process_urls(urls)
            finally:
                os.unlink(tmp_path)

    if "multiple_info_list" in st.session_state and st.session_state.multiple_info_list:
        _render_results()


def _process_urls(urls: list):
    playlist_service = PlaylistService()
    download_service = DownloadManagerService()
    
    individual_urls = []
    playlist_entries = []
    playlist_summary = []
    skipped_items = []
    
    for url in urls:
        if URLCleanerService.is_playlist_url(url):
            try:
                entries = playlist_service.get_playlist_entries(url)
                playlist_entries.extend(entries)
                playlist_summary.append({
                    "url": url,
                    "title": entries[0].get("playlist_title", "Playlist") if entries else "Playlist",
                    "count": len(entries)
                })
            except Exception as e:
                skipped_items.append(f"Playlist: {clean_error_message(str(e))}")
        else:
            individual_urls.append(url)
    
    st.session_state.all_video_urls = []
    st.session_state.multiple_info_list = []
    
    total_items = len(individual_urls) + len(playlist_entries)
    progress_bar = st.progress(0)
    processed = 0
    
    with st.status(f"Obteniendo información de {total_items} videos...", expanded=True):
        for url in individual_urls:
            try:
                info = download_service.get_video_info(url)
                info['_url'] = url
                info['_source'] = 'individual'
                st.session_state.multiple_info_list.append(info)
                st.session_state.all_video_urls.append(url)
            except Exception as e:
                skipped_items.append(f"{url}: {clean_error_message(str(e))}")
            processed += 1
            progress_bar.progress(processed / total_items)
        
        for entry in playlist_entries:
            try:
                info = download_service.get_video_info(entry['url'])
                info['_url'] = entry['url']
                info['_source'] = 'playlist'
                info['_playlist_title'] = entry.get('playlist_title', 'Playlist')
                st.session_state.multiple_info_list.append(info)
                st.session_state.all_video_urls.append(entry['url'])
            except Exception as e:
                skipped_items.append(f"{entry['url']}: {clean_error_message(str(e))}")
            processed += 1
            progress_bar.progress(processed / total_items)
    
    if playlist_summary:
        summary_text = " | ".join([f"{p['title']} ({p['count']} videos)" for p in playlist_summary])
        st.info(f"📚 Playlists detectadas: {summary_text}")
    
    if skipped_items:
        with st.expander(f"⚠️ {len(skipped_items)} video(s) no pudieron procesarse"):
            for item in skipped_items:
                st.markdown(f"- {item}")
    
    st.success(f"✅ {len(st.session_state.multiple_info_list)} videos listos para descargar.")


def _render_results():
    st.markdown("---")
    st.subheader(f"Videos encontrados ({len(st.session_state.multiple_info_list)})")
    
    with st.container(height=400):
        for info in st.session_state.multiple_info_list:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(info.get('thumbnail', ''), width=120)
            with col2:
                source_badge = "📚 Playlist" if info.get('_source') == 'playlist' else "🎬 Individual"
                st.markdown(f"**{info.get('title', 'Sin título')}**")
                st.caption(f"{source_badge} | Canal: {info.get('uploader', 'Desconocido')} | Duración: {info.get('duration', 'N/A')}s")
            st.divider()
    
    st.markdown("---")
    st.subheader("Acciones de descarga")
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1.2])
    with col1:
        batch_type = st.radio("Tipo", ["Video", "Audio (MP3)"], horizontal=True, key="batch_type_radio")
    
    with col2:
        if batch_type == "Video":
            batch_quality = st.selectbox("Calidad", ["best", "1080", "720", "480"], index=0, key="batch_q_vid_sel")
        else:
            batch_quality = st.selectbox("Calidad", ["320", "192", "128", "best"], index=0, key="batch_q_aud_sel")
            
    with col3:
        max_workers = st.selectbox("Descargas simultáneas", [1, 2, 3, 4, 5], index=2, key="max_workers_sel", help="Recomendado: 3")
            
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        is_downloading = st.session_state.get("is_downloading", False)
        
        if st.button("🚀 Iniciar Descarga Masiva", type="primary", width="stretch", disabled=is_downloading, key="btn_start_mass_download"):
            st.session_state.is_downloading = True
            _execute_batch_download_parallel(batch_type, batch_quality, max_workers)
            st.session_state.is_downloading = False
            st.rerun()


def _execute_batch_download_parallel(download_type: str, quality: str, max_workers: int):
    urls = st.session_state.all_video_urls
    project_name = st.session_state.get("multi_project_name", "Proyecto_Multiple")
    
    project_manager = ProjectManagerService()
    project = project_manager.create_project(name=project_name, is_single_session=False)
    
    download_manager = DownloadManagerService()
    
    with st.status("Procesando descargas en paralelo...", expanded=True):
        st.markdown(f"**Proyecto:** `{project.base_path.name}` | **Hilos:** {max_workers}")
        
        tasks = download_manager.download_batch_parallel(
            urls=urls,
            download_type=download_type,
            quality=quality,
            project=project,
            max_workers=max_workers
        )
        
        render_parallel_progress(tasks, len(urls))
        
        completed = sum(1 for t in tasks if t.status == "completed")
        st.success(f"✅ Proceso finalizado: {completed}/{len(urls)} archivos guardados.")