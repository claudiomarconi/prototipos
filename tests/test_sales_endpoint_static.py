import re
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "ConsumoApiAgilleControl" / "MainForm.pas"


def _method_body(method_name: str) -> str:
    source = SOURCE.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"^(procedure|function)\s+TfrmMain\.{re.escape(method_name)}\b.*?"
        r"(?=^(procedure|function)\s+TfrmMain\.|\binitialization\b)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(source)
    if not match:
        raise AssertionError(f"Method TfrmMain.{method_name} not found")
    return match.group(0)


class SalesEndpointStaticTests(unittest.TestCase):
    def test_invoice_header_is_created_inside_transaction(self):
        body = _method_body("GravarNotaFiscal")

        self.assertLess(
            body.index("FClient.Orm.TransactionBegin(TOrmNotaFiscal);"),
            body.index("NotaFiscal := ProcessarNotaFiscal(AVendaAgille);"),
        )
        self.assertRegex(
            body,
            r"except\s+FClient\.Orm\.RollBack;\s+raise;",
            "failed sales must roll back and propagate the error",
        )

    def test_client_reference_uses_its_own_autofree_holder(self):
        body = _method_body("ProcessarNotaFiscal")

        self.assertIn(
            "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF)",
            body,
        )
        self.assertNotIn(
            "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF)",
            body,
        )


if __name__ == "__main__":
    unittest.main()
