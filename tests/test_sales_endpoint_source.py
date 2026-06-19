import re
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "ConsumoApiAgilleControl" / "MainForm.pas"


def read_source():
    return SOURCE.read_text(encoding="cp1252")


def routine_body(source, name):
    match = re.search(
        rf"{re.escape(name)}.*?begin(?P<body>.*?)\nend;",
        source,
        re.DOTALL | re.IGNORECASE,
    )
    assert match, f"{name} not found"
    return match.group("body")


def test_sales_write_is_fully_transactional():
    body = routine_body(read_source(), "procedure TfrmMain.GravarNotaFiscal")

    transaction_pos = body.index("FClient.Orm.TransactionBegin(TOrmNotaFiscal)")
    note_pos = body.index("NotaFiscal := ProcessarNotaFiscal(AVendaAgille)")
    item_pos = body.index("ProcessarItensNotaFiscal(AVendaAgille, NotaFiscal)")
    parcel_pos = body.index("ProcessarParcelasNotaFiscal(AVendaAgille)")
    commit_pos = body.index("FClient.Orm.Commit")

    assert transaction_pos < note_pos < item_pos < parcel_pos < commit_pos
    assert re.search(r"except.*FClient\.Orm\.RollBack;.*raise;", body, re.DOTALL)


def test_customer_ref_uses_its_own_autofree_owner():
    body = routine_body(read_source(), "function TfrmMain.ProcessarNotaFiscal")

    assert (
        "oClient       := TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF);"
        in body
    )
    assert "TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, GrupoEmpresaAF)" not in body
