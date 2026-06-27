import re
import unittest
from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "ConsumoApiAgilleControl"
    / "MainForm.pas"
)


def read_source():
    return SOURCE.read_text(encoding="cp1252")


def extract_routine(source, name):
    pattern = re.compile(
        rf"(?:procedure|function)\s+TfrmMain\.{name}\b.*?"
        rf"(?=\n(?:procedure|function)\s+TfrmMain\.|\ninitialization\b)",
        re.DOTALL,
    )
    match = pattern.search(source)
    if not match:
        raise AssertionError(f"Routine {name} not found")
    return match.group(0)


class SalesPersistenceSourceTests(unittest.TestCase):
    def test_invoice_header_is_saved_inside_transaction(self):
        routine = extract_routine(read_source(), "GravarNotaFiscal")

        transaction = routine.index("FClient.Orm.TransactionBegin(TOrmNotaFiscal);")
        invoice = routine.index("NotaFiscal := ProcessarNotaFiscal(AVendaAgille);")
        items = routine.index("ProcessarItensNotaFiscal(AVendaAgille, NotaFiscal);")
        payments = routine.index("ProcessarParcelasNotaFiscal(AVendaAgille);")
        commit = routine.index("FClient.Orm.Commit;")

        self.assertLess(transaction, invoice)
        self.assertLess(invoice, items)
        self.assertLess(items, payments)
        self.assertLess(payments, commit)

    def test_transaction_failures_rollback_and_are_not_swallowed(self):
        routine = extract_routine(read_source(), "GravarNotaFiscal")
        rollback = routine.index("FClient.Orm.RollBack;")
        reraises = routine.index("raise;")

        self.assertIn("except", routine)
        self.assertLess(rollback, reraises)

    def test_client_lookup_uses_its_own_autofree_holder(self):
        routine = extract_routine(read_source(), "ProcessarNotaFiscal")

        self.assertIn("EmpresaAF, GrupoEmpresaAF, ClienteAF: IAutoFree;", routine)
        self.assertIn(
            "oGrupoEmpresa := TOrmRefHelper.Ref<TOrmGrupoEmpresa>(2, GrupoEmpresaAF);",
            routine,
        )
        self.assertIn(
            "oClient       := TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF);",
            routine,
        )
        self.assertNotIn(
            "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF)",
            routine,
        )


if __name__ == "__main__":
    unittest.main()
