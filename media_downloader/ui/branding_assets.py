from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BRANDING_ROOT = PROJECT_ROOT / "branding"


def _first_existing(paths: list[Path]) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def get_brand_assets() -> dict[str, Path | None]:
    logo_dark = _first_existing(
        [
            BRANDING_ROOT / "logo" / "LOGO_LETRAS_CLARAS.png",
            BRANDING_ROOT / "logo" / "LOGO_DYT.png",
            BRANDING_ROOT / "logo" / "LOGO_LETRAS_OSCURAS.png",
        ]
    )
    logo_light = _first_existing(
        [
            BRANDING_ROOT / "logo" / "LOGO_LETRAS_OSCURAS.png",
            BRANDING_ROOT / "logo" / "LOGO_DYT.png",
            BRANDING_ROOT / "logo" / "LOGO_LETRAS_CLARAS.png",
        ]
    )
    banner_dark = _first_existing(
        [
            BRANDING_ROOT / "images" / "TITULO_SUBTITULO_OSCURO.png",
            BRANDING_ROOT / "images" / "TITULO_SUBTITULO_CLARO.png",
            BRANDING_ROOT / "images" / "TITULO_OSCURO.png",
        ]
    )
    banner_light = _first_existing(
        [
            BRANDING_ROOT / "images" / "TITULO_SUBTITULO_CLARO.png",
            BRANDING_ROOT / "images" / "TITULO_SUBTITULO_OSCURO.png",
            BRANDING_ROOT / "images" / "TITULO_OSCURO.png",
        ]
    )

    return {
        "logo_dark": logo_dark,
        "logo_light": logo_light,
        "banner_dark": banner_dark,
        "banner_light": banner_light,
    }
