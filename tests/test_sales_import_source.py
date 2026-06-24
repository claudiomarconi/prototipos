import re
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "ConsumoApiAgilleControl" / "MainForm.pas"


def _mainform_source():
    return SOURCE.read_text(encoding="cp1252")


def _routine_body(source, routine_name):
    match = re.search(
        rf"{re.escape(routine_name)}.*?^begin$(.*?)^end;",
        source,
        re.DOTALL | re.MULTILINE,
    )
    if not match:
        raise AssertionError(f"Could not find routine body for {routine_name}")
    return match.group(1)


class SalesImportSourceTests(unittest.TestCase):
    def test_nota_header_is_inserted_inside_sales_transaction(self):
        body = _routine_body(
            _mainform_source(),
            "procedure TfrmMain.GravarNotaFiscal",
        )

        self.assertLess(
            body.index("TransactionBegin"),
            body.index("ProcessarNotaFiscal"),
        )
        self.assertLess(
            body.index("ProcessarNotaFiscal"),
            body.index("ProcessarItensNotaFiscal"),
        )
        self.assertIn("RollBack", body)
        self.assertIn("raise;", body)

    def test_cliente_reference_uses_its_own_lifetime_holder(self):
        body = _routine_body(
            _mainform_source(),
            "function TfrmMain.ProcessarNotaFiscal",
        )

        self.assertIn("TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF)", body)
        self.assertNotIn("TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF)", body)

    def test_item_timestamp_uses_payload_date_format(self):
        body = _routine_body(
            _mainform_source(),
            "procedure TfrmMain.ProcessarItensNotaFiscal",
        )

        self.assertIn("StrToDateTime(ProdutoAgille.DtHora_Venda)", body)
        self.assertNotIn("Iso8601ToDateTime(ProdutoAgille.DtHora_Venda)", body)


if __name__ == "__main__":
    unittest.main()
