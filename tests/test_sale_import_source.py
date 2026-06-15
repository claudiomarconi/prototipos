from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "ConsumoApiAgilleControl" / "MainForm.pas"


def read_main_form() -> str:
    return SOURCE.read_text(encoding="cp1252")


def extract_block(text: str, start: str, end: str) -> str:
    start_pos = text.index(start)
    end_pos = text.index(end, start_pos)
    return text[start_pos:end_pos]


def test_cliente_reference_uses_its_own_autofree_holder():
    source = read_main_form()

    assert (
        "oClient       := TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF);"
        in source
    )
    assert (
        "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF)"
        not in source
    )


def test_sale_header_insert_is_inside_transaction_and_failures_propagate():
    source = read_main_form()
    body = extract_block(
        source,
        "procedure TfrmMain.GravarNotaFiscal(const AVendaAgille: TVendaAgille);",
        "procedure TfrmMain.ProcessarItensNotaFiscal",
    )

    assert body.index("FClient.Orm.TransactionBegin(TOrmNotaFiscal);") < body.index(
        "NotaFiscal := ProcessarNotaFiscal(AVendaAgille);"
    )
    assert body.index("FClient.Orm.RollBack;") < body.index("raise;")
    assert "finally\n    NotaFiscal.Free;\n  end;" in body


def test_note_object_is_freed_if_header_creation_fails():
    source = read_main_form()
    body = extract_block(
        source,
        "function TfrmMain.ProcessarNotaFiscal(const AVendaAgille: TVendaAgille): TOrmNotaFiscal;",
        "procedure TfrmMain.ProcessarParcelasNotaFiscal",
    )

    assert body.index("NotaFiscal := TOrmNotaFiscal.Create;") < body.index("try")
    assert "except\n    NotaFiscal.Free;\n    raise;\n  end;" in body


def test_nested_record_json_types_are_registered_before_parent_sale_record():
    source = read_main_form()

    product_pos = source.index("TRttiJson.RegisterFromText(TypeInfo(TProdutoAgille)")
    parcel_pos = source.index("TRttiJson.RegisterFromText(TypeInfo(TParcelaAgille)")
    sale_pos = source.index("TRttiJson.RegisterFromText(TypeInfo(TVendaAgille)")

    assert product_pos < sale_pos
    assert parcel_pos < sale_pos
