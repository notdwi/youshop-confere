import json
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import httpx

from simulacoes.integracoes.extracao import ExtractionError, extract

TEXT = "Use ANACURSO e pague 20% a menos no plano Completo."
ITEMS = [{"id": "ana", "quote": TEXT, "internal": "somente para uso local"}]
CLAIM = {"kind": "coupon", "value": 20, "plan": "Completo", "coupon": "ANACURSO", "evidence": TEXT}
SETTINGS = {"CONFERE_MODE": "nvidia", "NVIDIA_MODEL": "fake/model", "NVIDIA_API_KEY": "test-only"}


class ExtractionTests(IsolatedAsyncioTestCase):
    async def invoke(self, output, status=200):
        def respond(request):
            body = json.loads(request.content)
            self.assertEqual(body["model"], SETTINGS["NVIDIA_MODEL"])
            self.assertEqual(json.loads(body["messages"][1]["content"]), [{"id": "ana", "quote": TEXT}])
            return httpx.Response(status, json={"choices": [{"finish_reason": "stop", "message": {
                "content": json.dumps({"campaigns": output})
            }}]})

        client = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        with patch("simulacoes.integracoes.extracao._config", return_value=SETTINGS), patch(
            "simulacoes.integracoes.nvidia.httpx.AsyncClient", return_value=client
        ):
            return await extract(ITEMS)

    async def test_recorded_text_is_matched_by_content(self):
        with patch("simulacoes.integracoes.extracao._config", return_value={}):
            self.assertEqual((await extract(ITEMS))["ana"][0].value, 20)
            edit = [{"id": "ana", "quote": TEXT.replace("20", "30")}]
            self.assertEqual((await extract(edit))["ana"][0].kind, "unknown")

    async def test_valid_provider_response(self):
        claims = await self.invoke([{"id": "ana", "claims": [CLAIM]}])
        self.assertEqual(claims["ana"][0].evidence, TEXT)

    async def test_reject_invalid_responses(self):
        good = {"id": "ana", "claims": [CLAIM]}
        for batch in [[], [good, good], [{**good, "id": "bruno"}],
                      [{"id": "ana", "claims": [{**CLAIM, "evidence": "frase inventada"}]}],
                      [{"id": "ana", "claims": [{**CLAIM, "value": True}]}]]:
            with self.subTest(batch=batch), self.assertRaises(ExtractionError):
                await self.invoke(batch)

    async def test_provider_failure_stays_visible(self):
        with self.assertRaises(ExtractionError):
            await self.invoke([], status=429)

    async def test_explicit_brl_is_returned_in_cents(self):
        quote = "O plano Básico hoje sai por R$ 99."
        data = {"kind": "price", "plan": "Básico", "value": 99, "evidence": quote}
        with patch.dict(ITEMS[0], {"quote": quote}), patch(__name__ + ".TEXT", quote):
            claims = await self.invoke([{"id": "ana", "claims": [data]}])
        self.assertEqual(claims["ana"][0].value, 9900)

    async def test_retry_incomplete_response_once(self):
        batches = [[], [{"id": "ana", "claims": [CLAIM]}]]
        def respond(request):
            content = json.dumps({"campaigns": batches.pop(0)})
            return httpx.Response(200, json={"choices": [{"finish_reason": "stop", "message": {"content": content}}]})
        client = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        with patch("simulacoes.integracoes.extracao._config", return_value=SETTINGS), patch(
            "simulacoes.integracoes.nvidia.httpx.AsyncClient", return_value=client
        ):
            result = await extract(ITEMS)
        self.assertEqual(result["ana"][0].value, 20)
        self.assertEqual(batches, [])
