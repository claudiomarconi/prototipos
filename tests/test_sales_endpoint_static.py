import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN_FORM = ROOT / "ConsumoApiAgilleControl" / "MainForm.pas"


def read_main_form() -> str:
    return MAIN_FORM.read_text(encoding="cp1252")


def method_body(source: str, signature: str) -> str:
    start = source.index(signature)
    next_method = re.search(r"\n(?:procedure|function) TfrmMain\.", source[start + 1 :])
    if next_method is None:
        raise AssertionError(f"Could not find end of {signature}")
    end = start + 1 + next_method.start()
    return source[start:end]


class SalesEndpointStaticTests(unittest.TestCase):
    def test_sales_persistence_is_wrapped_in_one_transaction(self) -> None:
        body = method_body(
            read_main_form(),
            "procedure TfrmMain.GravarNotaFiscal(const AVendaAgille: TVendaAgille);",
        )

        self.assertLess(body.index("TransactionBegin"), body.index("ProcessarNotaFiscal"))
        self.assertLess(body.index("ProcessarNotaFiscal"), body.index("ProcessarItensNotaFiscal"))
        self.assertLess(body.index("ProcessarItensNotaFiscal"), body.index("ProcessarParcelasNotaFiscal"))
        self.assertLess(body.index("ProcessarParcelasNotaFiscal"), body.index("Commit"))
        self.assertRegex(body, r"except\s+FClient\.Orm\.RollBack;\s+raise;")

    def test_sales_path_initializes_and_authenticates_client(self) -> None:
        source = read_main_form()
        gravar = method_body(
            source,
            "procedure TfrmMain.GravarNotaFiscal(const AVendaAgille: TVendaAgille);",
        )
        autenticar = method_body(source, "function TfrmMain.AutenticarCliente: Boolean;")

        self.assertIn("if not AutenticarCliente then", gravar)
        self.assertIn("ConectarCliente;", autenticar)
        self.assertIn("FClient.SetUser('cmarcony', 'synopse')", autenticar)

    def test_cliente_reference_uses_own_autofree_lifetime(self) -> None:
        body = method_body(
            read_main_form(),
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

    def test_agille_item_dates_use_local_datetime_format(self) -> None:
        body = method_body(
            read_main_form(),
            "procedure TfrmMain.ProcessarItensNotaFiscal(const AVendaAgille: TVendaAgille;",
        )

        self.assertIn("item.dt_movimento := StrToDateTime(ProdutoAgille.DtHora_Venda);", body)
        self.assertNotIn("Iso8601ToDateTime(ProdutoAgille.DtHora_Venda)", body)


if __name__ == "__main__":
    unittest.main()
