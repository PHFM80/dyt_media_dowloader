#main.py
import streamlit as st


def main():
    # Lazy imports para evitar ScriptRunContext warnings
    from ui.pages.home import render_home
    from ui.pages.single_download import render_single_download
    from ui.pages.multiple_download import render_multiple_download
    
    st.set_page_config(
        page_title="Descargar YouTube",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
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
elif st.runtime.exists():
    # Para Streamlit Cloud
    main()