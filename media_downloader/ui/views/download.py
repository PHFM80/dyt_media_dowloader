from __future__ import annotations

from pathlib import Path

import streamlit as st

from media_downloader.config import DOWNLOADS_ROOT
from media_downloader.integrations.ffmpeg_tools import ffmpeg_is_available
from media_downloader.integrations.ytdlp_client import YtDlpClient
from media_downloader.models import DownloadProject
from media_downloader.services.download_service import DownloadService
from media_downloader.services.input_parser import parse_text_input
from media_downloader.ui.common import render_local_image, scroll_to_top, format_file_size
from media_downloader.ui.session import create_new_project, read_uploaded_urls
from media_downloader.services.project_service import list_project_files


def render_download_view(assets: dict[str, Path | None]) -> None:
    scroll_to_top()
    st.sidebar.subheader("Navegación")
    if st.sidebar.button("Volver al inicio", width="stretch"):
        st.session_state.view = "home"
        st.rerun()

    if assets["logo_light"]:
        st.sidebar.image(str(assets["logo_light"]), width="stretch")

    title_col, image_col = st.columns([1.08, 0.92], vertical_alignment="center")
    with title_col:
        st.markdown('<div class="download-header-title">Media Downloader</div>', unsafe_allow_html=True)
    with image_col:
        if assets["banner_dark"]:
            render_local_image(assets["banner_dark"], max_height=170, fit="cover")
        elif assets["logo_dark"]:
            render_local_image(assets["logo_dark"], max_height=170, fit="cover")

    project_name = st.text_input(
        "Nombre del proyecto",
        key="project_name",
        placeholder="Ejemplo: musica_abril",
    )
    if st.button("Crear o reiniciar proyecto", width="stretch"):
        create_new_project(project_name)
        st.rerun()

    project: DownloadProject = st.session_state.project
    st.info(f"Proyecto activo: `{project.name}` | Carpeta: `{project.folder}`")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Entradas")
        pasted_urls = st.text_area(
            "Pegue una o varias URLs",
            placeholder="Una URL por linea o varias URLs separadas por texto",
            height=180,
        )
        uploaded_file = st.file_uploader("Subir archivo TXT o DOCX", type=["txt", "docx"])
        mode = st.radio("Tipo de descarga", ["video", "audio"], horizontal=True)

        pending_urls = parse_text_input(pasted_urls).urls
        if uploaded_file is not None:
            try:
                pending_urls.extend(read_uploaded_urls(uploaded_file))
            except Exception as exc:  # noqa: BLE001
                st.error(f"No se pudo leer el archivo cargado: {exc}")
        pending_urls = list(dict.fromkeys(pending_urls))

        st.session_state.pending_urls = pending_urls

        st.info(f"URLs detectadas: {len(pending_urls)}")
        if pending_urls:
            st.code("\n".join(pending_urls), language="text")
            
            # Mostrar formatos disponibles para la primera URL
            if mode == "video" and len(pending_urls) > 0:
                first_url = pending_urls[0]
                st.subheader("Formatos disponibles")
                with st.spinner(f"Analizando formatos de: {first_url}..."):
                    try:
                        client = YtDlpClient(st.session_state.project.folder)
                        formats_data = client.list_formats(first_url)
                        
                        # Verificar si hay error
                        if "error" in formats_data:
                            st.warning(f"⚠️ No se pudo analizar los formatos del video: {formats_data['error'][:100]}...")
                            st.info("Se usará el **mejor formato automático disponible** al descargar.")
                            st.session_state.selected_video_format = None
                            st.session_state.selected_audio_format = None
                        else:
                            video_formats = formats_data.get("videos", [])
                            audio_formats = formats_data.get("audios", [])
                            is_combined = formats_data.get("combined", False)
                            
                            if not is_combined and video_formats and audio_formats:
                                col_vid, col_aud = st.columns(2)
                                with col_vid:
                                    st.write("**Selecciona Video:**")
                                    video_options = [f["label"] for f in video_formats]
                                    selected_video = st.selectbox("Video", video_options, key="video_format")
                                    selected_video_id = next(f["id"] for f in video_formats if f["label"] == selected_video)
                                
                                with col_aud:
                                    st.write("**Selecciona Audio:**")
                                    audio_options = [f["label"] for f in audio_formats]
                                    selected_audio = st.selectbox("Audio", audio_options, key="audio_format")
                                    selected_audio_id = next(f["id"] for f in audio_formats if f["label"] == selected_audio)
                                
                                st.session_state.selected_video_format = selected_video_id
                                st.session_state.selected_audio_format = selected_audio_id
                                st.success("✅ Formatos seleccionados correctamente")
                            else:
                                st.info("💡 El video tiene **formato combinado** (sin separación video/audio).")
                                st.info("Se descargará automáticamente en la mejor calidad disponible.")
                                st.session_state.selected_video_format = None
                                st.session_state.selected_audio_format = None
                    except Exception as exc:  # noqa: BLE001
                        st.warning(f"⚠️ No se pudieron obtener los formatos: {str(exc)[:150]}...")
                        st.info("Se usará el **mejor formato automático disponible** al descargar.")
                        st.session_state.selected_video_format = None
                        st.session_state.selected_audio_format = None

        ffmpeg_ready = ffmpeg_is_available()
        start_disabled = not pending_urls or not ffmpeg_ready
        if not ffmpeg_ready:
            st.warning("Falta ffmpeg o ffprobe. Instala ambos antes de iniciar descargas de video o mp3.")

        if st.button("Iniciar descargas", type="primary", width="stretch", disabled=start_disabled):
            service = DownloadService()
            progress_bar = st.progress(0)
            status_box = st.empty()

            def on_progress(index: int, total: int, current_url: str) -> None:
                progress_bar.progress((index - 1) / max(total, 1))
                status_box.write(f"Procesando {index}/{total}: {current_url}")

            # Pasar formatos seleccionados si están disponibles
            video_fmt = st.session_state.get("selected_video_format")
            audio_fmt = st.session_state.get("selected_audio_format")
            
            st.session_state.results = service.process_urls(
                st.session_state.project,
                pending_urls,
                mode,
                on_progress=on_progress,
                video_format=video_fmt,
                audio_format=audio_fmt,
            )
            progress_bar.progress(1.0)
            status_box.success("Proceso finalizado")

    with col_right:
        st.subheader("Estado")
        st.metric("Proyecto activo", st.session_state.project.slug)
        st.metric("URLs en cola", len(st.session_state.pending_urls))
        st.metric("Carpeta raiz", str(DOWNLOADS_ROOT))

        if st.session_state.results:
            st.subheader("Resultados")
            for result in st.session_state.results:
                if result.status == "completed":
                    details = result.message
                    if result.output_path:
                        details = f"{details} | {result.output_path}"
                    st.success(f"{result.title}: {details}")
                else:
                    st.error(f"{result.url}: {result.message}")

    st.write("")
    st.divider()
    
    # Mostrar archivos acumulados en el proyecto
    project_files = list_project_files(st.session_state.project.folder)
    if project_files:
        st.subheader("📁 Archivos acumulados en el proyecto")
        st.info(f"Total: {len(project_files)} archivo(s) en `{st.session_state.project.name}`")
        
        for idx, file_info in enumerate(project_files, 1):
            from datetime import datetime
            mod_time = datetime.fromtimestamp(file_info["modified"]).strftime("%Y-%m-%d %H:%M:%S")
            file_size = format_file_size(file_info["size"])
            st.caption(f"{idx}. **{file_info['name']}** | {file_size} | {mod_time}")
    
    st.write("")
    st.divider()
    left_spacer, center_col, right_spacer = st.columns([2, 1.1, 2])
    with center_col:
        if st.button("Volver al inicio", width="content"):
            st.session_state.view = "home"
            st.rerun()
