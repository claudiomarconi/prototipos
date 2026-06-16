import re
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "ConsumoApiAgilleControl" / "MainForm.pas"


def read_source() -> str:
    return SOURCE.read_text(encoding="cp1252")


def procedure_body(source: str, signature: str) -> str:
    match = re.search(
        rf"{re.escape(signature)}(?P<body>.*?)(?=^procedure TfrmMain\.|^function TfrmMain\.|^initialization)",
        source,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise AssertionError(f"Could not find body for {signature}")
    return match.group("body")


class MainFormSaveFlowTests(unittest.TestCase):
    def test_note_is_inserted_inside_transaction_and_failures_propagate(self) -> None:
        body = procedure_body(
            read_source(),
            "procedure TfrmMain.GravarNotaFiscal(const AVendaAgille: TVendaAgille);",
        )

        transaction_index = body.index("FClient.Orm.TransactionBegin(TOrmNotaFiscal);")
        note_index = body.index("NotaFiscal := ProcessarNotaFiscal(AVendaAgille);")

        self.assertLess(transaction_index, note_index)
        self.assertIn("if not FClient.Orm.TransactionBegin(TOrmNotaFiscal) then", body)
        self.assertIn("FClient.Orm.RollBack;", body)
        self.assertRegex(body, r"FClient\.Orm\.RollBack;\s+raise;")
        self.assertNotRegex(body, r"ProcessarNotaFiscal\(AVendaAgille\);\s+FClient\.Orm\.TransactionBegin")

    def test_orm_add_failures_are_checked_before_continuing(self) -> None:
        source = read_source()

        self.assertIn("if FClient.Orm.Add(NotaFiscal, True) = 0 then", source)
        self.assertIn("if FClient.Orm.Add(Item, True) = 0 then", source)
        self.assertIn("if FClient.Orm.Add(Financeiro, True) = 0 then", source)

    def test_item_timestamp_uses_payload_date_format_parser(self) -> None:
        source = read_source()

        self.assertIn("StrToDateTime(ProdutoAgille.DtHora_Venda)", source)
        self.assertNotIn("Iso8601ToDateTime(ProdutoAgille.DtHora_Venda)", source)

    def test_client_reference_uses_its_own_autofree_holder(self) -> None:
        source = read_source()

        self.assertIn(
            "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF)",
            source,
        )
        self.assertNotIn(
            "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF)",
            source,
        )


if __name__ == "__main__":
    unittest.main()
