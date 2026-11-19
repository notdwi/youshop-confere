import json
import os
from typing import Literal

from mcp.server.fastmcp import FastMCP

from ..checkout import Proposal, checkout, offer

server = FastMCP("YouShop Confere")
proposal = Proposal.model_validate(json.loads(os.environ["CONFERE_PROPOSAL"]))
Version = Literal["atual", "proposta"]


@server.tool()
def consultar_oferta(version: Version) -> dict[str, object]:
    """Consulta as regras e preços do cenário isolado desta análise."""
    return offer(proposal, version)


@server.tool()
def simular_checkout(version: Version, campaign_id: str, plan: str, coupon: str | None = None) -> dict[str, object]:
    """Calcula um checkout fictício para o vínculo cadastrado, em centavos."""
    return checkout(proposal, version, campaign_id, plan, coupon)


if __name__ == "__main__":
    server.run(transport="stdio")
