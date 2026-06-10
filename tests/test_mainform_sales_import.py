import re
import unittest
from pathlib import Path


MAIN_FORM = Path(__file__).resolve().parents[1] / "ConsumoApiAgilleControl" / "MainForm.pas"


def read_mainform() -> str:
    return MAIN_FORM.read_text(encoding="cp1252")


def routine_body(source: str, signature: str) -> str:
    pattern = re.compile(
        rf"{re.escape(signature)}.*?^end;",
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(source)
    if not match:
        raise AssertionError(f"Could not find routine {signature!r}")
    return match.group(0)


class SalesImportRegressionTests(unittest.TestCase):
    def test_customer_reference_uses_independent_autofree_owner(self) -> None:
        source = read_mainform()
        body = routine_body(
            source,
            "function TfrmMain.ProcessarNotaFiscal(const AVendaAgille: TVendaAgille): TOrmNotaFiscal;",
        )

        self.assertIn(
            "oClient       := TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF);",
            body,
        )
        self.assertNotIn(
            "oClient       := TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF);",
            body,
        )

    def test_nota_fiscal_insert_is_inside_rollbackable_transaction(self) -> None:
        source = read_mainform()
        body = routine_body(
            source,
            "procedure TfrmMain.GravarNotaFiscal(const AVendaAgille: TVendaAgille);",
        )

        transaction_pos = body.index("FClient.Orm.TransactionBegin(TOrmNotaFiscal);")
        nota_pos = body.index("NotaFiscal := ProcessarNotaFiscal(AVendaAgille);")
        item_pos = body.index("ProcessarItensNotaFiscal(AVendaAgille, NotaFiscal);")

        self.assertLess(transaction_pos, nota_pos)
        self.assertLess(nota_pos, item_pos)
        self.assertIn("FClient.Orm.RollBack;", body)
        self.assertIn("raise;", body)


if __name__ == "__main__":
    unittest.main()
