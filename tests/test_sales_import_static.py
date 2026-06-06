from pathlib import Path
import re
import unittest


SOURCE = Path(__file__).resolve().parents[1] / "ConsumoApiAgilleControl" / "MainForm.pas"


def method_body(source: str, name: str) -> str:
    match = re.search(
        rf"(?:procedure|function)\s+TfrmMain\.{re.escape(name)}\b.*?^end;",
        source,
        flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise AssertionError(f"{name} not found")
    return match.group(0)


class SalesImportStaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = SOURCE.read_text(encoding="cp1252")

    def test_sales_import_is_wrapped_in_transaction(self) -> None:
        body = method_body(self.source, "GravarNotaFiscal")

        transaction_begin = body.index("TransactionBegin(TOrmNotaFiscal)")
        nota_insert = body.index("ProcessarNotaFiscal(AVendaAgille)")
        commit = body.index("FClient.Orm.Commit")

        self.assertLess(transaction_begin, nota_insert)
        self.assertLess(nota_insert, commit)
        self.assertIn("FClient.Orm.RollBack", body)
        self.assertRegex(body, r"FClient\.Orm\.RollBack;\s+raise;")

    def test_cliente_ref_uses_own_autofree_holder(self) -> None:
        body = method_body(self.source, "ProcessarNotaFiscal")

        self.assertIn(
            "oClient       := TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF);",
            body,
        )
        self.assertNotIn(
            "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF)",
            body,
        )

    def test_orm_insert_failures_abort_import(self) -> None:
        for name in ("ProcessarNotaFiscal", "ProcessarItensNotaFiscal", "ProcessarParcelasNotaFiscal"):
            with self.subTest(method=name):
                body = method_body(self.source, name)
                self.assertIn("FClient.Orm.Add", body)
                self.assertRegex(body, r"(FClient\.Orm\.Add\([^)]*\)|IDValue)\s*=\s*0")
                self.assertIn("raise Exception.Create", body)

    def test_endpoint_requires_connection_before_import(self) -> None:
        body = method_body(self.source, "Button2Click")

        self.assertIn("if not Assigned(FClient) then", body)
        self.assertIn("Conecte ao servidor antes de enviar vendas.", body)

    def test_sample_item_timestamp_uses_local_datetime_parser(self) -> None:
        body = method_body(self.source, "ProcessarItensNotaFiscal")

        self.assertIn("StrToDateTime(ProdutoAgille.DtHora_Venda)", body)
        self.assertNotIn("Iso8601ToDateTime(ProdutoAgille.DtHora_Venda)", body)


if __name__ == "__main__":
    unittest.main()
