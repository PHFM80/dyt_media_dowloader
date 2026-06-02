from __future__ import annotations

import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            :root {
                --bg-dark: #0B1F3A;
                --primary: #0A66C2;
                --accent: #22C7F2;
                --surface: #F4F7FA;
                --text: #1F2937;
                --white: #FFFFFF;
                color-scheme: light;
            }
            html, body {
                color-scheme: light;
            }
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(34, 199, 242, 0.22), transparent 30%),
                    radial-gradient(circle at top right, rgba(10, 102, 194, 0.18), transparent 28%),
                    linear-gradient(180deg, #f8fbfe 0%, #f4f7fa 48%, #eef4fb 100%);
                color: var(--text);
            }
            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #0b1f3a 0%, #102a4d 100%);
            }
            section[data-testid="stSidebar"] * {
                color: white !important;
            }
            .brand-hero {
                background: linear-gradient(135deg, var(--bg-dark) 0%, #12345f 55%, var(--primary) 100%);
                color: white;
                border-radius: 28px;
                padding: 2rem;
                box-shadow: 0 20px 50px rgba(11, 31, 58, 0.20);
            }
            .brand-kicker {
                text-transform: uppercase;
                letter-spacing: .16em;
                font-size: .74rem;
                opacity: .8;
                margin-bottom: .75rem;
            }
            .brand-title {
                font-size: clamp(2rem, 5vw, 4.4rem);
                line-height: 1.02;
                font-weight: 800;
                margin: 0 0 1rem 0;
            }
            .stApp h1 {
                margin-top: 0.15rem;
                margin-bottom: 0.2rem;
            }
            .download-header-title {
                font-size: clamp(2.15rem, 3.4vw, 3.35rem);
                line-height: 1;
                font-weight: 800;
                color: var(--bg-dark);
                margin: 0;
                padding: 0;
                text-align: center;
            }
            .brand-copy {
                font-size: 1.05rem;
                line-height: 1.65;
                max-width: 62ch;
                opacity: .95;
            }
            .brand-pill {
                display: inline-block;
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.16);
                border-radius: 999px;
                padding: .5rem .9rem;
                margin: .35rem .45rem 0 0;
                font-size: .9rem;
            }
            .feature-card {
                background: rgba(255, 255, 255, 0.84);
                border: 1px solid rgba(31, 41, 55, 0.08);
                border-radius: 22px;
                padding: 1.2rem 1.15rem;
                box-shadow: 0 16px 40px rgba(31, 41, 55, 0.06);
                height: 100%;
            }
            .feature-card h3 {
                margin-top: 0;
                color: var(--bg-dark);
            }
            .soft-section {
                background: rgba(255, 255, 255, 0.72);
                border: 1px solid rgba(31, 41, 55, 0.08);
                border-radius: 24px;
                padding: 1.2rem 1.2rem 0.8rem;
                box-shadow: 0 16px 40px rgba(31, 41, 55, 0.05);
            }
            .contact-box {
                background: linear-gradient(135deg, #0b1f3a 0%, #12345f 100%);
                color: white;
                border-radius: 24px;
                padding: 1.25rem 1.25rem 1rem;
            }
            .contact-box a {
                color: #9eefff !important;
                text-decoration: none;
            }
            .tiny-note {
                font-size: .88rem;
                color: rgba(255,255,255,.82);
            }
            div[data-testid="stButton"] > button {
                border-radius: 999px;
                padding: 0.8rem 1.25rem;
                font-weight: 700;
                border: 0;
                background: linear-gradient(135deg, #0A66C2 0%, #22C7F2 100%);
                color: white;
            }
            div[data-testid="stButton"] > button:hover {
                opacity: .95;
                transform: translateY(-1px);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
