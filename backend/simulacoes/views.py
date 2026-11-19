import json
import asyncio
import logging
from threading import BoundedSemaphore

from pydantic import ValidationError

from django.core.exceptions import RequestDataTooBig
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from .checkout import CAMPAIGNS, CURRENT, INITIAL, REFERENCE, CURRENT_EXPIRY, Proposal
from .analise import analyze as analyze_proposal
from .integracoes.extracao import extraction_mode, ExtractionError


analysis_slots = BoundedSemaphore(2)


@require_GET
def demo(request):
    try:
        mode = extraction_mode()
    except ExtractionError as exc:
        return JsonResponse({"error": "Demonstração indisponível. Tente novamente mais tarde."}, status=503)
    return JsonResponse(dict(current={**CURRENT, "expiresAt": CURRENT_EXPIRY}, initialDraft=INITIAL, campaigns=CAMPAIGNS, referenceTime=REFERENCE, example=mode == "recorded"))


@require_POST
def analyze(request):
    if request.content_type != "application/json":
        return JsonResponse({"error": "Envie a proposta em JSON."}, status=415)
    try:
        draft = json.loads(request.body)
    except RequestDataTooBig:
        return JsonResponse({"error": "Proposta muito grande."}, status=413)
    except (ValueError, RecursionError):
        return JsonResponse({"error": "JSON inválido."}, status=400)
    try:
        proposal = Proposal.model_validate(draft)
    except ValidationError as exc:
        field = ".".join(map(str, exc.errors()[0]["loc"])) or "proposta"
        return JsonResponse({"error": f"Valor inválido em {field}."}, status=400)
    if not analysis_slots.acquire(blocking=False):
        return JsonResponse({"error": "Duas análises em andamento. Tente novamente em instantes."}, status=429)
    try:
        return JsonResponse(asyncio.run(analyze_proposal(proposal)))
    except ExtractionError as exc:
        return JsonResponse({"error": "A leitura das campanhas falhou. Tente simular novamente."}, status=502)
    except TimeoutError:
        return JsonResponse({"error": "A análise excedeu o tempo limite. Tente novamente."}, status=504)
    except Exception as exc:
        logging.getLogger("django").error("Falha na integração: %s", type(exc).__name__)
        return JsonResponse({"error": "Falha ao conferir o checkout. Tente novamente."}, status=502)
    finally:
        analysis_slots.release()
