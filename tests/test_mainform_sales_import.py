import unittest
from pathlib import Path


SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "ConsumoApiAgilleControl"
    / "MainForm.pas"
)


def read_source():
    return SOURCE_PATH.read_text(encoding="cp1252")


def section(source, start_marker, end_marker):
    start = source.index(start_marker)
    end = source.index(end_marker, start)
    return source[start:end]


class SalesImportSourceTests(unittest.TestCase):
    def test_customer_reference_uses_its_own_autofree_handle(self):
        source = read_source()
        body = section(
            source,
            "function TfrmMain.ProcessarNotaFiscal",
            "procedure TfrmMain.ProcessarParcelasNotaFiscal",
        )

        self.assertIn(
            "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF)",
            body,
        )
        self.assertNotIn(
            "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF)",
            body,
        )

    def test_parent_note_is_created_inside_rollback_scope(self):
        source = read_source()
        body = section(
            source,
            "procedure TfrmMain.GravarNotaFiscal",
            "procedure TfrmMain.ProcessarItensNotaFiscal",
        )

        self.assertLess(
            body.index("FClient.Orm.TransactionBegin(TOrmNotaFiscal);"),
            body.index("NotaFiscal := ProcessarNotaFiscal(AVendaAgille);"),
        )
        self.assertIn("FClient.Orm.RollBack;", body)
        self.assertIn("raise;", body)
        self.assertIn("NotaFiscal.Free;", body)

    def test_item_sale_timestamp_uses_agille_payload_format(self):
        source = read_source()
        body = section(
            source,
            "procedure TfrmMain.ProcessarItensNotaFiscal",
            "function TfrmMain.ProcessarNotaFiscal",
        )

        self.assertIn("StrToDateTime(ProdutoAgille.DtHora_Venda)", body)
        self.assertNotIn("Iso8601ToDateTime(ProdutoAgille.DtHora_Venda)", body)


if __name__ == "__main__":
    unittest.main()
