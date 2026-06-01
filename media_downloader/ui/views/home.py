from __future__ import annotations

from pathlib import Path

import streamlit as st

from media_downloader.ui.common import render_local_image, scroll_to_top


def render_home_view(assets: dict[str, Path | None]) -> None:
    scroll_to_top()
    hero_col, hero_side = st.columns([1.3, 0.9], vertical_alignment="center")
    with hero_col:
        st.markdown(
            """
            <div class="brand-hero">
                <div class="brand-kicker">Branding · Media Downloader</div>
                <div class="brand-title">Descargas multimedia con una experiencia limpia y profesional.</div>
                <div class="brand-copy">
                    Una aplicación local pensada para organizar descargas por proyecto, aceptar varias URLs o archivos
                    con enlaces, y mantener todo ordenado dentro de tu carpeta de descargas.
                </div>
                <div style="margin-top: 1rem;">
                    <span class="brand-pill">YouTube</span>
                    <span class="brand-pill">Audio y video</span>
                    <span class="brand-pill">Proyectos por sesión</span>
                    <span class="brand-pill">TXT y DOCX</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hero_side:
        if assets["banner_dark"]:
            render_local_image(assets["banner_dark"], max_height=120)
        elif assets["logo_dark"]:
            render_local_image(assets["logo_dark"], max_height=120)

    st.write("")
    feature_col_1, feature_col_2, feature_col_3 = st.columns(3)

    with feature_col_1:
        st.markdown(
            """
            <div class="feature-card">
                <h3>1. Cargá tu contenido</h3>
                <p>Pegá una o varias URLs, o subí un archivo TXT o DOCX con enlaces listos para procesar.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with feature_col_2:
        st.markdown(
            """
            <div class="feature-card">
                <h3>2. Elegí tu proyecto</h3>
                <p>Nombrá la sesión de descarga para agrupar todo en una misma carpeta y mantener el orden.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with feature_col_3:
        st.markdown(
            """
            <div class="feature-card">
                <h3>3. Descargá y organizá</h3>
                <p>La app crea una estructura limpia dentro de Downloads y procesa audio o video según lo que elijas.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    expl_col, info_col = st.columns([1.1, 0.9], gap="large")

    with expl_col:
        st.markdown(
            """
            <div class="soft-section">
                <h3 style="margin-top:0;color:#0B1F3A;">Como funciona</h3>
                <ol>
                    <li>Elegis un nombre de proyecto.</li>
                    <li>Pegas URLs o subis un TXT/DOCX.</li>
                    <li>La app arma una cola interna.</li>
                    <li>Descarga todo dentro de una carpeta unica.</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with info_col:
        st.markdown(
            """
            <div class="contact-box">
                <h3 style="margin-top:0;">Contacto</h3>
                <p><strong>Correo:</strong> <a href="mailto:dytdigitaliza@gmail.com">dytdigitaliza@gmail.com</a></p>
                <p><strong>Empresa:</strong> +54 9 2612 35-4493</p>
                <p><strong>Asesor:</strong> Pablo Flores · +5492617678889</p>
                <p class="tiny-note">Soporte y acompañamiento para el proyecto y su puesta en marcha.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    center_left, center_col, center_right = st.columns([2, 1.1, 2])
    with center_col:
        if st.button("Ir a la descarga", type="primary", width="content"):
            st.session_state.view = "download"
            st.rerun()
