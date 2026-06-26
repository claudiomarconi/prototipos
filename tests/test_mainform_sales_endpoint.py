from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "ConsumoApiAgilleControl" / "MainForm.pas").read_text(
    encoding="cp1252"
)
SAMPLE_JSON = (ROOT / "ConsumoApiAgilleControl" / "venda-agille.json").read_text(
    encoding="utf-8"
)


def _section(start_marker: str, end_marker: str) -> str:
    start = SOURCE.index(start_marker)
    end = SOURCE.index(end_marker, start)
    return SOURCE[start:end]


class SalesEndpointSourceTests(unittest.TestCase):
    def test_sales_write_wraps_invoice_items_and_payments_in_one_transaction(self):
        body = _section(
            "procedure TfrmMain.GravarNotaFiscal",
            "procedure TfrmMain.ProcessarItensNotaFiscal",
        )

        self.assertLess(
            body.index("FClient.Orm.TransactionBegin(TOrmNotaFiscal);"),
            body.index("NotaFiscal := ProcessarNotaFiscal(AVendaAgille);"),
        )
        self.assertLess(
            body.index("NotaFiscal := ProcessarNotaFiscal(AVendaAgille);"),
            body.index("ProcessarItensNotaFiscal(AVendaAgille, NotaFiscal);"),
        )
        self.assertLess(
            body.index("ProcessarItensNotaFiscal(AVendaAgille, NotaFiscal);"),
            body.index("ProcessarParcelasNotaFiscal(AVendaAgille);"),
        )
        self.assertIn("FClient.Orm.RollBack;", body)
        self.assertIn("raise;", body)
        self.assertIn("NotaFiscal.Free;", body)

    def test_customer_reference_does_not_reuse_group_company_autofree_holder(self):
        body = _section(
            "function TfrmMain.ProcessarNotaFiscal",
            "procedure TfrmMain.ProcessarParcelasNotaFiscal",
        )

        self.assertIn(
            "oClient       := TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF);",
            body,
        )
        self.assertNotIn(
            "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF)",
            body,
        )

    def test_item_timestamp_parser_accepts_sample_sales_payload_format(self):
        body = _section(
            "procedure TfrmMain.ProcessarItensNotaFiscal",
            "function TfrmMain.ProcessarNotaFiscal",
        )

        self.assertIn('"DtHora_Venda": "01/09/2025 11:42"', SAMPLE_JSON)
        self.assertIn("item.dt_movimento := StrToDateTime(ProdutoAgille.DtHora_Venda);", body)
        self.assertNotIn("Iso8601ToDateTime(ProdutoAgille.DtHora_Venda)", body)


if __name__ == "__main__":
    unittest.main()
