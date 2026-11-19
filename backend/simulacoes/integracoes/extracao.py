import os
from pathlib import Path

from django.core.cache import cache
from dotenv import dotenv_values

from ..checkout import CAMPAIGNS
from .contratos import Claim, ExtractionError
from .nvidia import DEFAULT_FALLBACK, extract_nvidia

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


def _config():
    return {**dotenv_values(ENV_FILE, interpolate=False), **os.environ}


def extraction_mode():
    mode = _config().get("CONFERE_MODE", "recorded")
    if mode not in ("nvidia", "recorded"):
        raise ExtractionError("Modo de extração inválido no backend.")
    return mode


RECORDED = {
    "Use ANACURSO e pague 20% a menos no plano Completo.":
        dict(kind="coupon", plan="Completo", value=20, coupon="ANACURSO"),
    "Com meu link, o plano Básico sai por R$ 99.":
        dict(kind="price", plan="Básico", value=9900),
}

async def extract(campaigns):
    texts = {item["id"]: item["quote"] for item in campaigns}
    if extraction_mode() == "recorded":
        return {
            key: [Claim(evidence=text, **RECORDED.get(text, {"kind": "unknown"}))]
            for key, text in texts.items()
        }

    settings = _config()
    demo_texts = {c["id"]: c["quote"] for c in CAMPAIGNS if c["inSimulation"]}
    if texts != demo_texts:
        return await extract_nvidia(texts, settings)

    cache_key = f"demo-claims:v1:{settings.get('NVIDIA_MODEL')}:{settings.get('NVIDIA_FALLBACK_MODEL', DEFAULT_FALLBACK)}"
    claims = cache.get(cache_key)
    if claims is None:
        claims = await extract_nvidia(texts, settings)
        cache.set(cache_key, claims, timeout=900)
    return claims
