from __future__ import annotations

import base64
import io
from pathlib import Path

import streamlit as st
from PIL import Image, ImageChops


def trim_image(image: Image.Image) -> Image.Image:
    rgba_image = image.convert("RGBA")
    alpha_bbox = rgba_image.getchannel("A").getbbox()
    if alpha_bbox:
        bbox = alpha_bbox
    else:
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


def render_local_image(image_path: Path, max_height: int, fit: str = "contain") -> None:
    with Image.open(image_path) as image:
        trimmed = trim_image(image)
        output = io.BytesIO()
        trimmed.save(output, format="PNG")
        image_data = base64.b64encode(output.getvalue()).decode("ascii")

    st.markdown(
        f"""
        <div style="display:flex; align-items:center; justify-content:center; width:100%; height:{max_height}px; margin:0; padding:0; line-height:0; overflow:hidden; border-radius:18px;">
            <img
                src="data:image/png;base64,{image_data}"
                style="display:block; width:100%; height:100%; object-fit:{fit}; object-position:center center; margin:0; padding:0;"
            />
        </div>
        """,
        unsafe_allow_html=True,
    )


def scroll_to_top() -> None:
    st.html(
        """
        <script>
            window.scrollTo({ top: 0, left: 0, behavior: "instant" });
        </script>
        """,
        unsafe_allow_javascript=True,
    )
