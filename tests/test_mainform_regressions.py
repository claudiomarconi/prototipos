import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN_FORM = ROOT / "ConsumoApiAgilleControl" / "MainForm.pas"
SAMPLE_SALE = ROOT / "ConsumoApiAgilleControl" / "venda-agille.json"


def read_main_form() -> str:
    return MAIN_FORM.read_text(encoding="cp1252")


def extract_procedure(source: str, name: str) -> str:
    pattern = rf"(procedure TfrmMain\.{re.escape(name)}.*?)(?=\n(?:procedure|function) TfrmMain\.|\ninitialization)"
    match = re.search(pattern, source, flags=re.DOTALL)
    if not match:
        raise AssertionError(f"procedure {name} not found")
    return match.group(1)


class MainFormSaleImportRegressionTests(unittest.TestCase):
    def test_sale_import_is_one_transaction_and_failures_propagate(self):
        procedure = extract_procedure(read_main_form(), "GravarNotaFiscal")

        transaction_begin = procedure.index("FClient.Orm.TransactionBegin")
        header_insert = procedure.index("NotaFiscal := ProcessarNotaFiscal")
        item_insert = procedure.index("ProcessarItensNotaFiscal")
        payment_insert = procedure.index("ProcessarParcelasNotaFiscal")
        commit = procedure.index("FClient.Orm.Commit")

        self.assertLess(transaction_begin, header_insert)
        self.assertLess(header_insert, item_insert)
        self.assertLess(item_insert, payment_insert)
        self.assertLess(payment_insert, commit)
        self.assertIn("FClient.Orm.RollBack;", procedure)
        self.assertIn("raise;", procedure)
        self.assertIn("NotaFiscal.Free;", procedure)

    def test_buttons_authenticate_client_before_using_rest_client(self):
        source = read_main_form()
        button1 = extract_procedure(source, "Button1Click")
        button2 = extract_procedure(source, "Button2Click")
        ensure_client = extract_procedure(source, "EnsureClientAuthenticated")

        self.assertLess(button1.index("EnsureClientAuthenticated;"), button1.index("FClient.ExecuteList"))
        self.assertLess(button2.index("EnsureClientAuthenticated;"), button2.index("GravarNotaFiscal"))
        self.assertIn("FClient := TRestHttpClient.Create", ensure_client)
        self.assertIn("FClient.SetUser", ensure_client)
        self.assertIn("raise Exception.Create", ensure_client)

    def test_sample_sale_dates_use_supported_parser(self):
        source = read_main_form()
        sample = json.loads(SAMPLE_SALE.read_text(encoding="utf-8"))
        sale_dates = [product["DtHora_Venda"] for product in sample["Produtos"]]

        self.assertTrue(all("/" in value and "T" not in value for value in sale_dates))
        self.assertNotIn("Iso8601ToDateTime(ProdutoAgille.DtHora_Venda)", source)
        self.assertIn("StrToDateTime(ProdutoAgille.DtHora_Venda)", source)

    def test_cliente_reference_uses_its_own_autofree_holder(self):
        source = read_main_form()

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
