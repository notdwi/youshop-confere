import json
from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, StrictInt, field_validator

CAMPAIGNS = json.loads((Path(__file__).parent / "dados" / "campanhas.json").read_text())
CURRENT = {"scope": "Todos", "discount": 20}
INITIAL = {"scope": "Básico", "discount": 20}
REFERENCE = "2026-11-18T12:00:00-03:00"
CURRENT_EXPIRY = "2026-12-31T23:59:59-03:00"
PRICES = {"Básico": 9900, "Completo": 19900}
LINKS = {"ana": "Completo", "bruno": "Básico", "camila": "Completo"}


class Proposal(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True)
    scope: Literal["Todos", "Básico", "Completo"]
    discount: StrictInt = Field(ge=0, le=100)
    expiresAt: AwareDatetime | None = datetime.fromisoformat(CURRENT_EXPIRY)
    referenceTime: AwareDatetime = datetime.fromisoformat(REFERENCE)
    texts: dict[str, str] = Field(default_factory=dict)

    @field_validator("expiresAt", "referenceTime", mode="before")
    @classmethod
    def iso_date(cls, value):
        if value is None or isinstance(value, datetime):
            return value
        if not isinstance(value, str) or "T" not in value:
            raise ValueError("Informe uma data ISO com horário e fuso.")
        return datetime.fromisoformat(value)

    @field_validator("texts")
    @classmethod
    def campaign_texts(cls, values):
        if any(key not in LINKS or not text.strip() or len(text) > 800 for key, text in values.items()):
            raise ValueError("Use campanhas vinculadas e legendas entre 1 e 800 caracteres.")
        return values


def offer(proposal, version):
    rules = CURRENT if version == "atual" else proposal.model_dump(mode="json")
    return {"prices": PRICES, "coupon": "ANACURSO", "scope": rules["scope"],
            "discount": rules["discount"], "expiresAt": rules.get("expiresAt", CURRENT_EXPIRY)}


def checkout(proposal, version, campaign_id, plan, coupon):
    if LINKS.get(campaign_id) != plan or plan not in PRICES:
        return {"resolved": False, "reason": "O link cadastrado não confirma o plano anunciado."}
    rules = offer(proposal, version)
    percent = 0
    reason = "Preço do plano sem cupom."
    if coupon:
        if coupon.upper() != rules["coupon"]:
            reason = "Código de cupom desconhecido."
        elif rules["scope"] not in ("Todos", plan):
            reason = "O plano não é elegível para o cupom."
        elif rules["expiresAt"] and proposal.referenceTime > datetime.fromisoformat(rules["expiresAt"]):
            reason = "O cupom expirou no instante simulado."
        else:
            percent = rules["discount"]
            reason = "Cupom aplicado."
    total = PRICES[plan] - (PRICES[plan] * percent + 50) // 100
    return {"resolved": True, "total": total, "percent": percent, "applied": reason == "Cupom aplicado.", "reason": reason}
