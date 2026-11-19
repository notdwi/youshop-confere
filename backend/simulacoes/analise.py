import asyncio
import logging
import sys
from pathlib import Path
from uuid import uuid4

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from .integracoes.extracao import extract, extraction_mode
from .checkout import CAMPAIGNS

logger = logging.getLogger("django")
PRIORITY = ["Impactada", "Divergência preexistente", "Revisão necessária", "Compatível"]


def matches(claim, checkout):
    if claim.kind == "coupon":
        return checkout["applied"] and claim.value == checkout["percent"]
    return claim.value == checkout["total"]


async def compare(call, campaign_id, claim):
    result = dict(evidence=claim.evidence, status="Revisão necessária", before=None, after=None,
                  reason="Faltam condições explícitas para conferir a promessa.")
    if claim.kind == "unknown" or not claim.plan:
        return result
    params = dict(campaign_id=campaign_id, plan=claim.plan, coupon=claim.coupon)
    old = await call("simular_checkout", dict(version="atual", **params))
    new = await call("simular_checkout", dict(version="proposta", **params))
    if not old["resolved"] or not new["resolved"]:
        return {**result, "reason": new["reason"]}
    was, now = matches(claim, old), matches(claim, new)
    if now:
        status = "Compatível"
        reason = "A condição anunciada continua válida." if was else "A proposta corrige a divergência anterior."
    else:
        status = "Impactada" if was else "Divergência preexistente"
        reason = f"A condição anunciada diverge do checkout proposto. {new['reason']}"
    return dict(evidence=claim.evidence, status=status, reason=reason, before=old["total"], after=new["total"])


async def analyze(proposal):
    analysis_id = uuid4().hex
    campaigns = [{**c, "quote": proposal.texts.get(c["id"], c["quote"])}
                 for c in CAMPAIGNS if c["inSimulation"]]
    params = StdioServerParameters(command=sys.executable, args=["-m", "simulacoes.integracoes.mcp_server"],
                                   cwd=str(Path(__file__).resolve().parents[1]),
                                   env={"CONFERE_PROPOSAL": proposal.model_dump_json(exclude={"texts"})})
    async with asyncio.timeout(90):
        claims = await extract(campaigns)
        async with stdio_client(params) as streams, ClientSession(*streams) as session:
            await session.initialize()
            tools = await session.list_tools()
            if not {"consultar_oferta", "simular_checkout"} <= {tool.name for tool in tools.tools}:
                raise RuntimeError("Ferramentas MCP indisponíveis.")
            async def call(name, args):
                reply = await session.call_tool(name, args)
                if reply.isError or not isinstance(reply.structuredContent, dict):
                    raise RuntimeError("Falha na ferramenta MCP.")
                logger.info("analysis=%s tool=%s version=%s", analysis_id, name, args["version"])
                return reply.structuredContent
            for version in ("atual", "proposta"):
                await call("consultar_oferta", {"version": version})
            results = []
            for campaign in campaigns:
                details = [await compare(call, campaign["id"], claim) for claim in claims[campaign["id"]]]
                main = min(details, key=lambda d: PRIORITY.index(d["status"]))
                results.append({**main, "campaign": campaign, "details": details})
    return dict(results=results, example=extraction_mode() == "recorded", analysisId=analysis_id)
