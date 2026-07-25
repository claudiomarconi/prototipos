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


class ItemProductForeignKeySourceTests(unittest.TestCase):
    def test_item_assigns_product_fk_from_ref(self):
        routine = extract_routine(read_source(), "ProcessarItensNotaFiscal")

        ref = routine.index(
            "oProduto := TOrmRefHelper.Ref<TOrmProduto>(ProdutoAgille.Cod_Produto, ProdutoAF );"
        )
        assign = routine.index("Item.id_produto := oProduto.AsTOrm;")
        add = routine.index("FClient.Orm.Add(Item, True);")

        self.assertLess(ref, assign)
        self.assertLess(assign, add)

    def test_item_still_links_invoice_before_insert(self):
        routine = extract_routine(read_source(), "ProcessarItensNotaFiscal")

        invoice = routine.index("Item.id_nota_fiscal := ANotaFiscal.AsTOrm;")
        product = routine.index("Item.id_produto := oProduto.AsTOrm;")
        add = routine.index("FClient.Orm.Add(Item, True);")

        self.assertLess(invoice, add)
        self.assertLess(product, add)


if __name__ == "__main__":
    unittest.main()
