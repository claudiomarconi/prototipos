from pathlib import Path
import unittest


SOURCE = Path(__file__).resolve().parents[1] / "ConsumoApiAgilleControl" / "MainForm.pas"


def _source_text() -> str:
    return SOURCE.read_text(encoding="latin-1")


class MainFormRegressionTests(unittest.TestCase):
    def test_sale_header_is_inserted_inside_transaction(self) -> None:
        source = _source_text()
        transaction_pos = source.index("FClient.Orm.TransactionBegin(TOrmNotaFiscal)")
        header_pos = source.index("NotaFiscal := ProcessarNotaFiscal(AVendaAgille)")

        self.assertLess(transaction_pos, header_pos)

    def test_cliente_reference_uses_its_own_autofree_holder(self) -> None:
        source = _source_text()

        self.assertIn("TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF)", source)
        self.assertNotIn("TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF)", source)


if __name__ == "__main__":
    unittest.main()
