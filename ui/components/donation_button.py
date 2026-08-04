import streamlit as st

def render_donation_button():
    """Renderiza el botón de donación con enlace a Cafecito"""
    st.markdown("---")
    st.markdown("### ☕ Apoyar el proyecto")
    st.markdown("Si esta herramienta te resulta útil, podés invitarme un cafecito:")
    st.markdown(
        '[![Invitame un café en cafecito.app](https://cdn.cafecito.app/imgs/buttons/button_1.svg)](https://cafecito.app/dyt-digitaliza)',
        unsafe_allow_html=True
    )