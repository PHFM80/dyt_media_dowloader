from __future__ import annotations

from pathlib import Path

import streamlit as st

from media_downloader.config import DOWNLOADS_ROOT
from media_downloader.integrations.ffmpeg_tools import ffmpeg_is_available
from media_downloader.models import DownloadProject
from media_downloader.services.download_service import DownloadService
from media_downloader.services.input_parser import parse_text_input
from media_downloader.ui.common import render_local_image, scroll_to_top
from media_downloader.ui.session import create_new_project, read_uploaded_urls


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

            st.session_state.results = service.process_urls(
                st.session_state.project,
                pending_urls,
                mode,
                on_progress=on_progress,
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
    left_spacer, center_col, right_spacer = st.columns([2, 1.1, 2])
    with center_col:
        if st.button("Volver al inicio", width="content"):
            st.session_state.view = "home"
            st.rerun()
