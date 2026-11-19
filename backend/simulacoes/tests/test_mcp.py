import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from simulacoes.analise import analyze
from simulacoes.checkout import Proposal


class MCPIsolationTests(IsolatedAsyncioTestCase):
    @patch.dict("os.environ", {"CONFERE_MODE": "recorded"})
    async def test_simultaneous_checkouts_use_their_own_proposal(self):
        drafts = [Proposal(scope="Todos", discount=d) for d in (0, 50, 100)]
        reports = await asyncio.gather(*(analyze(draft) for draft in drafts))
        self.assertEqual([r["results"][0]["after"] for r in reports], [19900, 9950, 0])
        self.assertEqual(len({r["analysisId"] for r in reports}), len(drafts))
