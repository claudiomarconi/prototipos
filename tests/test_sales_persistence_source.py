import re
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "ConsumoApiAgilleControl" / "MainForm.pas"


def read_source() -> str:
    return SOURCE.read_text(encoding="cp1252")


class SalesPersistenceSourceTests(unittest.TestCase):
    def test_invoice_header_is_created_inside_sales_transaction(self) -> None:
        source = read_source()
        match = re.search(
            r"procedure TfrmMain\.GravarNotaFiscal\(const AVendaAgille: TVendaAgille\);"
            r"(?P<body>.*?)"
            r"\nend;\n\nprocedure TfrmMain\.ProcessarItensNotaFiscal",
            source,
            flags=re.S,
        )
        self.assertIsNotNone(match, "GravarNotaFiscal body not found")
        body = match.group("body")

        transaction_begin = body.index("FClient.Orm.TransactionBegin(TOrmNotaFiscal);")
        create_header = body.index("NotaFiscal := ProcessarNotaFiscal(AVendaAgille);")
        create_items = body.index("ProcessarItensNotaFiscal(AVendaAgille, NotaFiscal);")
        create_payments = body.index("ProcessarParcelasNotaFiscal(AVendaAgille);")
        commit = body.index("FClient.Orm.Commit;")
        rollback = body.index("FClient.Orm.RollBack;")

        self.assertLess(
            transaction_begin,
            create_header,
            "invoice header must be inserted after the transaction starts",
        )
        self.assertLess(create_header, create_items)
        self.assertLess(create_items, create_payments)
        self.assertLess(create_payments, commit)
        self.assertLess(commit, rollback)

    def test_client_reference_uses_its_own_autofree_owner(self) -> None:
        source = read_source()

        self.assertIn(
            "oGrupoEmpresa := TOrmRefHelper.Ref<TOrmGrupoEmpresa>(2, GrupoEmpresaAF);",
            source,
        )
        self.assertIn(
            "oClient       := TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF);",
            source,
        )
        self.assertNotIn(
            "oClient       := TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF);",
            source,
        )


if __name__ == "__main__":
    unittest.main()
