from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "ConsumoApiAgilleControl" / "MainForm.pas"


def _source_text() -> str:
    return SOURCE.read_text(encoding="utf-8")


def test_sale_header_is_inserted_inside_transaction() -> None:
    source = _source_text()
    transaction_pos = source.index("FClient.Orm.TransactionBegin(TOrmNotaFiscal)")
    header_pos = source.index("NotaFiscal := ProcessarNotaFiscal(AVendaAgille)")

    assert transaction_pos < header_pos


def test_cliente_reference_uses_its_own_autofree_holder() -> None:
    source = _source_text()

    assert "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF)" in source
    assert "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF)" not in source
