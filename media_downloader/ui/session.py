from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from media_downloader.services.input_parser import parse_docx_file, parse_txt_file
from media_downloader.services.project_service import create_project, ensure_download_root


def init_session_state() -> None:
    ensure_download_root()
    if "project" not in st.session_state:
        st.session_state.project = create_project("descarga")
    if "pending_urls" not in st.session_state:
        st.session_state.pending_urls = []
    if "results" not in st.session_state:
        st.session_state.results = []
    if "project_name" not in st.session_state:
        st.session_state.project_name = "descarga"
    if "view" not in st.session_state:
        st.session_state.view = "home"
    if "selected_video_format" not in st.session_state:
        st.session_state.selected_video_format = None
    if "selected_audio_format" not in st.session_state:
        st.session_state.selected_audio_format = None


def create_new_project(name: str) -> None:
    st.session_state.project = create_project(name)
    st.session_state.results = []
    st.session_state.pending_urls = []
    st.session_state.view = "download"


def read_uploaded_urls(uploaded_file) -> list[str]:
    suffix = Path(uploaded_file.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_path = Path(temp_file.name)

    try:
        if suffix == ".txt":
            return parse_txt_file(temp_path).urls
        if suffix == ".docx":
            return parse_docx_file(temp_path).urls
        return []
    finally:
        temp_path.unlink(missing_ok=True)

