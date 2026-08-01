#ui\app.py
import streamlit as st

st.set_page_config(
    page_title="Descargar YouTube",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

from pages.home import render_home
from pages.single_download import render_single_download
from pages.multiple_download import render_multiple_download


def main():
    if "page" not in st.session_state:
        st.session_state.page = "Inicio"
    
    st.sidebar.title("🎬 Descargar YouTube")
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🏠 Inicio", use_container_width=True):
        st.session_state.page = "Inicio"
        st.rerun()
    
    if st.sidebar.button("📹 Descarga Única", use_container_width=True):
        st.session_state.page = "Descarga Única"
        st.rerun()
    
    if st.sidebar.button("📋 Descarga Múltiple", use_container_width=True):
        st.session_state.page = "Descarga Múltiple"
        st.rerun()
    
    st.sidebar.markdown("---")
    
    if st.session_state.page == "Inicio":
        render_home()
    elif st.session_state.page == "Descarga Única":
        render_single_download()
    elif st.session_state.page == "Descarga Múltiple":
        render_multiple_download()


if __name__ == "__main__":
    main()