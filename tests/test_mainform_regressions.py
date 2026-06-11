import re
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MAINFORM = ROOT / "ConsumoApiAgilleControl" / "MainForm.pas"


def read_mainform() -> str:
    return MAINFORM.read_text(encoding="cp1252")


def procedure_body(source: str, name: str) -> str:
    pattern = (
        rf"procedure TfrmMain\.{re.escape(name)}\(.*?"
        r"(?=\n(?:procedure|function) TfrmMain\.)"
    )
    match = re.search(pattern, source, re.S)
    if not match:
        raise AssertionError(f"procedure {name} not found")
    return match.group(0)


class MainFormRegressionTests(unittest.TestCase):
    def test_invoice_insert_is_inside_rollback_scope(self) -> None:
        body = procedure_body(read_mainform(), "GravarNotaFiscal")

        transaction_pos = body.index("FClient.Orm.TransactionBegin(TOrmNotaFiscal);")
        invoice_pos = body.index("NotaFiscal := ProcessarNotaFiscal(AVendaAgille);")
        commit_pos = body.index("FClient.Orm.Commit;")

        self.assertLess(transaction_pos, invoice_pos)
        self.assertLess(invoice_pos, commit_pos)
        self.assertIn("FClient.Orm.RollBack;", body)
        self.assertIn("raise;", body)

    def test_cliente_ref_uses_its_own_autofree_holder(self) -> None:
        source = read_mainform()

        self.assertIn(
            "oClient       := TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF);",
            source,
        )
        self.assertNotIn(
            "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF)",
            source,
        )

    def test_agille_item_datetime_uses_payload_format(self) -> None:
        source = read_mainform()

        self.assertIn(
            "item.dt_movimento := StrToDateTime(ProdutoAgille.DtHora_Venda);",
            source,
        )
        self.assertNotIn("Iso8601ToDateTime(ProdutoAgille.DtHora_Venda)", source)


if __name__ == "__main__":
    unittest.main()
