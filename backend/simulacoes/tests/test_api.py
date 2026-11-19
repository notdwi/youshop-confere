import os
from unittest.mock import patch

from django.test import SimpleTestCase


@patch.dict(os.environ, {"CONFERE_MODE": "recorded"})
class AnalysisTests(SimpleTestCase):
    def post(self, data):
        return self.client.post("/api/analises/", data, content_type="application/json")

    def test_demo_and_offer_changes(self):
        demo = self.client.get("/api/demo/").json()
        self.assertEqual(len(demo["campaigns"]), 7)
        results = self.post(demo["initialDraft"]).json()["results"]
        self.assertEqual([r["status"] for r in results], ["Impactada", "Compatível", "Revisão necessária"])
        self.assertEqual((results[0]["before"], results[0]["after"]), (15920, 19900))
        self.assertEqual(self.post(demo["current"]).json()["results"][0]["status"], "Compatível")
        for discount, cents in [(0, 19900), (10, 17910), (100, 0)]:
            self.assertEqual(self.post({"scope": "Todos", "discount": discount}).json()["results"][0]["after"], cents)

    def test_invalid_requests(self):
        for value in [-1, 101, True, 1.5, "20", None]:
            self.assertEqual(self.post({"scope": "Todos", "discount": value}).status_code, 400)
        for data in [{}, [], {"scope": "outro", "discount": 20}, {"scope": "Todos", "discount": 20, "extra": 1}]:
            self.assertEqual(self.post(data).status_code, 400)
        self.assertEqual(self.post("{").status_code, 400)
        self.assertEqual(self.post(" " * 16385).status_code, 413)
        self.assertEqual(self.client.get("/api/analises/").status_code, 405)
        self.assertEqual(self.client.post("/api/analises/", {}).status_code, 415)

    def test_expiry_boundary_and_recovery(self):
        future = "2027-01-01T12:00:00-03:00"
        for end, expected in [(future, "Compatível"), ("2027-01-01T11:59:59-03:00", "Divergência preexistente"), (None, "Compatível")]:
            data = {"scope": "Todos", "discount": 20, "referenceTime": future, "expiresAt": end}
            result = self.post(data).json()["results"][0]
            self.assertEqual(result["status"], expected)
            self.assertEqual(result["before"], 19900)

    def test_edited_unknown_and_invalid_context(self):
        data = {"scope": "Todos", "discount": 20}
        result = self.post({**data, "texts": {"ana": "Oferta personalizada"}}).json()["results"][0]
        self.assertEqual(result["status"], "Revisão necessária")
        self.assertEqual(result["evidence"], "Oferta personalizada")
        for invalid in [{"referenceTime": "2026-01-01T00:00"}, {"texts": {"extra": "Oi"}}, {"texts": {"ana": " "}}]:
            self.assertEqual(self.post({**data, **invalid}).status_code, 400)
