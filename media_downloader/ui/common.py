from __future__ import annotations

import base64
import io
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageChops


def trim_image(image: Image.Image) -> Image.Image:
    rgba_image = image.convert("RGBA")
    background = Image.new("RGBA", rgba_image.size, (255, 255, 255, 255))
    diff = ImageChops.difference(rgba_image, background)
    grayscale = diff.convert("L")
    mask = grayscale.point(lambda pixel: 255 if pixel > 18 else 0)
    bbox = mask.getbbox()
    if not bbox:
        return rgba_image

    left, top, right, bottom = bbox
    padding = 24
    left = max(left - padding, 0)
    top = max(top - padding, 0)
    right = min(right + padding, rgba_image.width)
    bottom = min(bottom + padding, rgba_image.height)
    return rgba_image.crop((left, top, right, bottom))


def render_local_image(image_path: Path, max_height: int) -> None:
    with Image.open(image_path) as image:
        trimmed = trim_image(image)
        output = io.BytesIO()
        trimmed.save(output, format="PNG")
        image_data = base64.b64encode(output.getvalue()).decode("ascii")

    st.markdown(
        f"""
        <div style="display:flex; align-items:center; justify-content:center; width:100%; margin:0; padding:0; line-height:0;">
            <img
                src="data:image/png;base64,{image_data}"
                style="display:block; width:100%; height:{max_height}px; object-fit:cover; object-position:center center; margin:0; padding:0; border-radius:18px;"
            />
        </div>
        """,
        unsafe_allow_html=True,
    )


def scroll_to_top() -> None:
    components.html(
        """
        <script>
            window.scrollTo({ top: 0, left: 0, behavior: "instant" });
        </script>
        """,
        height=0,
        width=0,
    )

