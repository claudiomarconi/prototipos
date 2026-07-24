import re
import unittest
from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "ConsumoApiAgilleControl"
    / "MainForm.pas"
)
SAMPLE_JSON = (
    Path(__file__).resolve().parents[1]
    / "ConsumoApiAgilleControl"
    / "venda-agille.json"
)


def read_source():
    return SOURCE.read_text(encoding="cp1252")


def extract_routine(source, name):
    pattern = re.compile(
        rf"(?:procedure|function)\s+TfrmMain\.{name}\b.*?"
        rf"(?=\n(?:procedure|function)\s+TfrmMain\.|\ninitialization\b)",
        re.DOTALL,
    )
    match = pattern.search(source)
    if not match:
        raise AssertionError(f"Routine {name} not found")
    return match.group(0)


class ItemDateTimeParsingSourceTests(unittest.TestCase):
    def test_sample_payload_uses_brazilian_datetime_not_iso8601(self):
        payload = SAMPLE_JSON.read_text(encoding="utf-8")
        self.assertRegex(payload, r'"DtHora_Venda"\s*:\s*"\d{2}/\d{2}/\d{4} \d{2}:\d{2}"')
        self.assertNotRegex(payload, r'"DtHora_Venda"\s*:\s*"\d{4}-\d{2}-\d{2}')

    def test_item_movement_uses_strtodatetime_not_iso8601(self):
        routine = extract_routine(read_source(), "ProcessarItensNotaFiscal")

        self.assertIn("StrToDateTime(ProdutoAgille.DtHora_Venda)", routine)
        self.assertNotIn("Iso8601ToDateTime(ProdutoAgille.DtHora_Venda)", routine)

    def test_invoice_and_payment_dates_remain_locale_parsers(self):
        invoice = extract_routine(read_source(), "ProcessarNotaFiscal")
        payments = extract_routine(read_source(), "ProcessarParcelasNotaFiscal")

        self.assertIn("StrToDate(AVendaAgille.Dt_Venda)", invoice)
        self.assertIn("StrToDate(Parcela.DataParcelas)", payments)


if __name__ == "__main__":
    unittest.main()
