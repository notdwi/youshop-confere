from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ExtractionError(RuntimeError):
    """Mensagem segura para o operador, sem resposta bruta nem credencial."""


class Claim(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    kind: Literal["price", "coupon", "unknown"]
    plan: Literal["Básico", "Completo"] | None = None
    value: int | None = Field(default=None, ge=0)
    coupon: str | None = Field(default=None, min_length=1, max_length=64)
    evidence: str = Field(min_length=1, max_length=4096)

    @model_validator(mode="after")
    def check_condition(self):
        if not self.evidence.strip():
            raise ValueError("Evidência vazia.")
        if self.kind == "unknown":
            if any(v is not None for v in (self.value, self.plan, self.coupon)):
                raise ValueError("Condição ambígua com detalhes inferidos.")
        elif self.value is None or self.plan is None:
            raise ValueError("Condição sem plano ou valor.")
        elif self.kind == "coupon" and (self.value > 100 or not self.coupon):
            raise ValueError("Cupom incompleto.")
        elif self.kind == "price" and self.coupon is not None:
            raise ValueError("Preço absoluto com cupom.")
        return self


class CampaignClaims(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    id: str
    claims: list[Claim] = Field(min_length=1, max_length=12)


class ExtractionBatch(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    campaigns: list[CampaignClaims]
