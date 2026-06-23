from pathlib import Path
import unittest


SOURCE = (Path(__file__).resolve().parents[1] / "ConsumoApiAgilleControl" / "MainForm.pas").read_text(
    encoding="cp1252"
)


def source_between(start_marker: str, end_marker: str) -> str:
    start = SOURCE.index(start_marker)
    end = SOURCE.index(end_marker, start)
    return SOURCE[start:end]


class SalesEndpointSourceTests(unittest.TestCase):
    def test_sale_header_is_created_inside_rollbackable_transaction(self) -> None:
        body = source_between(
            "procedure TfrmMain.GravarNotaFiscal",
            "procedure TfrmMain.ProcessarItensNotaFiscal",
        )

        self.assertLess(body.index("TransactionBegin"), body.index("ProcessarNotaFiscal"))
        self.assertLess(body.index("ProcessarNotaFiscal"), body.index("ProcessarItensNotaFiscal"))
        self.assertLess(body.index("ProcessarItensNotaFiscal"), body.index("ProcessarParcelasNotaFiscal"))
        self.assertLess(body.index("ProcessarParcelasNotaFiscal"), body.index("Commit"))
        self.assertIn("RollBack", body)
        self.assertIn("raise;", body)
        self.assertIn("NotaFiscal.Free", body)

    def test_failed_adds_abort_the_sale_save(self) -> None:
        self.assertIn("if FClient.Orm.Add(NotaFiscal, True) = 0 then", SOURCE)
        self.assertIn("if FClient.Orm.Add(Item, True) = 0 then", SOURCE)
        self.assertIn("if FClient.Orm.Add(Financeiro, True) = 0 then", SOURCE)

    def test_client_reference_uses_its_own_autofree_owner(self) -> None:
        self.assertIn(
            "oClient       := TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF);",
            SOURCE,
        )

    def test_agille_item_dates_use_payload_format(self) -> None:
        self.assertIn("item.dt_movimento := StrToDateTime(ProdutoAgille.DtHora_Venda);", SOURCE)
        self.assertNotIn("Iso8601ToDateTime(ProdutoAgille.DtHora_Venda)", SOURCE)


if __name__ == "__main__":
    unittest.main()
