from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MAIN_FORM = ROOT / "ConsumoApiAgilleControl" / "MainForm.pas"


def read_main_form() -> str:
    return MAIN_FORM.read_text(encoding="cp1252")


def extract_procedure(source: str, name: str) -> str:
    match = re.search(
        rf"procedure TfrmMain\.{re.escape(name)}\b.*?^end;",
        source,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise AssertionError(f"procedure {name} not found")
    return match.group(0)


class MainFormSourceTests(unittest.TestCase):
    def test_sales_import_transaction_wraps_note_and_children(self) -> None:
        body = extract_procedure(read_main_form(), "GravarNotaFiscal")

        transaction_pos = body.index("FClient.Orm.TransactionBegin(TOrmNotaFiscal);")
        note_pos = body.index("NotaFiscal := ProcessarNotaFiscal(AVendaAgille);")
        item_pos = body.index("ProcessarItensNotaFiscal(AVendaAgille, NotaFiscal);")
        parcelas_pos = body.index("ProcessarParcelasNotaFiscal(AVendaAgille);")
        commit_pos = body.index("FClient.Orm.Commit;")

        self.assertLess(transaction_pos, note_pos)
        self.assertLess(note_pos, item_pos)
        self.assertLess(item_pos, parcelas_pos)
        self.assertLess(parcelas_pos, commit_pos)
        self.assertRegex(body, r"FClient\.Orm\.RollBack;\s+raise;")

    def test_cliente_reference_uses_its_own_autofree_owner(self) -> None:
        source = read_main_form()

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
