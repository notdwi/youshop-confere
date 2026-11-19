import os
from pathlib import Path

from dotenv import dotenv_values

from .contratos import Claim, ExtractionError
from .nvidia import extract_nvidia

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

    return await extract_nvidia(texts, _config())
