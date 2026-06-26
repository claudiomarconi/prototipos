from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "ConsumoApiAgilleControl" / "MainForm.pas").read_text(
    encoding="cp1252"
)
SAMPLE_JSON = (ROOT / "ConsumoApiAgilleControl" / "venda-agille.json").read_text(
    encoding="utf-8"
)


def _section(start_marker: str, end_marker: str) -> str:
    start = SOURCE.index(start_marker)
    end = SOURCE.index(end_marker, start)
    return SOURCE[start:end]


def test_sales_write_wraps_invoice_items_and_payments_in_one_transaction():
    body = _section(
        "procedure TfrmMain.GravarNotaFiscal",
        "procedure TfrmMain.ProcessarItensNotaFiscal",
    )

    assert body.index("FClient.Orm.TransactionBegin(TOrmNotaFiscal);") < body.index(
        "NotaFiscal := ProcessarNotaFiscal(AVendaAgille);"
    )
    assert body.index("NotaFiscal := ProcessarNotaFiscal(AVendaAgille);") < body.index(
        "ProcessarItensNotaFiscal(AVendaAgille, NotaFiscal);"
    )
    assert body.index("ProcessarItensNotaFiscal(AVendaAgille, NotaFiscal);") < body.index(
        "ProcessarParcelasNotaFiscal(AVendaAgille);"
    )
    assert "FClient.Orm.RollBack;" in body
    assert "raise;" in body
    assert "NotaFiscal.Free;" in body


def test_customer_reference_does_not_reuse_group_company_autofree_holder():
    body = _section(
        "function TfrmMain.ProcessarNotaFiscal",
        "procedure TfrmMain.ProcessarParcelasNotaFiscal",
    )

    assert (
        "oClient       := TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF);"
        in body
    )
    assert (
        "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF)"
        not in body
    )


def test_item_timestamp_parser_accepts_sample_sales_payload_format():
    body = _section(
        "procedure TfrmMain.ProcessarItensNotaFiscal",
        "function TfrmMain.ProcessarNotaFiscal",
    )

    assert '"DtHora_Venda": "01/09/2025 11:42"' in SAMPLE_JSON
    assert "item.dt_movimento := StrToDateTime(ProdutoAgille.DtHora_Venda);" in body
    assert "Iso8601ToDateTime(ProdutoAgille.DtHora_Venda)" not in body
