from __future__ import annotations

import streamlit as st

from media_downloader.ui.branding_assets import get_brand_assets
from media_downloader.ui.session import init_session_state
from media_downloader.ui.styles import inject_styles
from media_downloader.ui.views.download import render_download_view
from media_downloader.ui.views.home import render_home_view


def run_app() -> None:
    st.set_page_config(page_title="D&T - Media Downloader", layout="wide")
    init_session_state()
    assets = get_brand_assets()
    inject_styles()

    if st.session_state.view == "home":
        render_home_view(assets)
    else:
        render_download_view(assets)

