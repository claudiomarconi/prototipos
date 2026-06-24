unit MainForm;
(*
  proximo end point:


EBD POINT VENDA PDV / WEB   ** vericiar viculacao empresa / prupo empresa
1 - dados nota
   ( cnpj,  data, numero id, numro nfe, numero pedido, valor, valor acrescimo, valor valor desconto,origem,  status, id_funcionario) 1-1
   tabelas ( notas_fiscais)

2 - dados cliente
   ( cpf /cnpj , Nome )  -
   tabela (clientes)  ** verificar se existe via cpf/cnpj

3 - dados item
    (id, qtd, valor unit, vl desconto, vl acrescimo, vl total) 1- n
   tabela (itens_notas_fiscais)

4 - dados recebimento
   (idForma, valor , idPlanoConta)  - n
  tabela (movimentos_financeiros

*)
interface

uses
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants, System.Classes, Vcl.Graphics,
  Vcl.StdCtrls, Vcl.Controls,

    mormot.core.os
  , mormot.rest.core
  , mormot.rest.http.client
  , mormot.orm.core
  , mormot.rest.client
  , mormot.db.core
  , mormot.soa.core
  , mormot.core.base
  , mormot.orm.base
  , mormot.crypt.core
  , mormot.core.collections
  , mormot.core.variants
  , mormot.db.rad.ui
  , mormot.db.rad.ui.orm
  , mormot.core.json
  , mormot.core.text
  , mormot.core.data
  , mormot.core.datetime

  , NotaFiscalOrm

  ,Vcl.Forms, Vcl.Dialogs, FireDAC.Stan.Intf, FireDAC.Stan.Option,
  FireDAC.Stan.Param, FireDAC.Stan.Error, FireDAC.DatS, FireDAC.Phys.Intf,
  FireDAC.DApt.Intf, FireDAC.Stan.Async, FireDAC.DApt, Data.DB, Vcl.Grids,
  Vcl.DBGrids, FireDAC.Comp.DataSet, FireDAC.Comp.Client;

type
(*
  TOrmBase = class(TOrm)
  private
    Fcriado_em: TDateTime;
    Fatualizado_em: TDateTime;
  public
  published
    property criado_em: TDateTime read Fcriado_em write Fcriado_em;
    property atualizado_em: TDateTime read Fatualizado_em write Fatualizado_em;
  end;

  TOrmCFOP = class(TOrmBase)
  private
    Fnu_cfop: RawUtf8;
    Fds_cfop: RawUtf8;
  published
    property nu_cfop: RawUtf8 read Fnu_cfop write Fnu_cfop;
    property ds_cfop: RawUtf8 read Fds_cfop write Fds_cfop;
  end;

  TOrmCEST = class(TOrmBase)
  private
    Fco_cest: RawUtf8;
    Fco_ncm: RawUtf8;
    Fds_descricao: RawUtf8;
  published
    property co_cest: RawUtf8 read Fco_cest write Fco_cest;
    property co_ncm: RawUtf8 read Fco_ncm write Fco_ncm;
    property ds_descricao: RawUtf8 read Fds_descricao write Fds_descricao;
  end;

  TOrmCST = class(TOrmBase)
  private
    Fds_descricao: RawUtf8;
    Ftp_regime_tributario: RawUtf8;
    Fco_cst: RawUtf8;
  published
    property co_cst: RawUtf8 read Fco_cst write Fco_cst;
    property ds_descricao: RawUtf8 read Fds_descricao write Fds_descricao;
    property tp_regime_tributario: RawUtf8 read Ftp_regime_tributario write Ftp_regime_tributario;
  end;

  TOrmNCM = class(TOrmBase)
  private
    Fds_descricao: RawUtf8;
    Fco_ncm: RawUtf8;
    Fdt_fim: TDate;
    Fdt_inicio: TDate;
  published
    property co_ncm: RawUtf8 read Fco_ncm write Fco_ncm;
    property ds_descricao: RawUtf8 read Fds_descricao write Fds_descricao;
    property dt_inicio: TDate read Fdt_inicio write Fdt_inicio;
    property dt_fim: TDate read Fdt_fim write Fdt_fim;
  end;

  TOrmGrupoEmpresa = class(TOrmBase)
  private
    Fds_descricao: RawUtf8;
  published
    property ds_descricao: RawUtf8 read Fds_descricao write Fds_descricao;
  end;

  TOrmGrupoImposto = class(TOrmBase)
  private
    Fid_cst: TOrmCST;
    Fds_descricao: RawUtf8;
    Ftx_reducao_icms: Currency;
    Fco_cst_pis: RawUtf8;
    Fco_cst_cofins: RawUtf8;
    Fid_grupo_empresa: TOrmGrupoEmpresa;
    Ftx_mva_fora: Currency;
    Ftx_icms_padrao: Currency;
    Fid_cfop: TOrmCFOP;
    Fds_nome: RawUtf8;
    Ftx_pis: Currency;
    Ftx_mva_padrao: Currency;
    Ftx_cofins: Currency;
    Forigem: Integer;
  published
    property ds_nome: RawUtf8 read Fds_nome write Fds_nome;
    property ds_descricao: RawUtf8 read Fds_descricao write Fds_descricao;
    property id_cfop: TOrmCFOP read Fid_cfop write Fid_cfop;
    property origem: Integer read Forigem write Forigem;
    property id_cst: TOrmCST read Fid_cst write Fid_cst;
    property co_cst_pis: RawUtf8 read Fco_cst_pis write Fco_cst_pis;
    property co_cst_cofins: RawUtf8 read Fco_cst_cofins write Fco_cst_cofins;
    property tx_pis: Currency read Ftx_pis write Ftx_pis;
    property tx_cofins: Currency read Ftx_cofins write Ftx_cofins;
    property tx_icms_padrao: Currency read Ftx_icms_padrao write Ftx_icms_padrao;
    property tx_reducao_icms: Currency read Ftx_reducao_icms write Ftx_reducao_icms;
    property tx_mva_padrao: Currency read Ftx_mva_padrao write Ftx_mva_padrao;
    property tx_mva_fora: Currency read Ftx_mva_fora write Ftx_mva_fora;
    property id_grupo_empresa: TOrmGrupoEmpresa read Fid_grupo_empresa write Fid_grupo_empresa;
  end;

  TOrmProduto = class(TOrmBase)
  private
    Fvl_compra: Currency;
    Fds_descricao: RawUtf8;
    Ftx_atualizacao_preco: Currency;
    Fqq_minima: Integer;
    Fco_cest: RawUtf8;
    Ffl_ativo: Boolean;
    Ftp_material: RawUtf8;
    Fds_unidade: RawUtf8;
    Fan_foto: RawUtf8;
    Fco_ncm: RawUtf8;
    Ffl_atualiza_compra: Boolean;
    Fvl_venda: Currency;
    Ffl_usa_pdv: Boolean;
    Ffl_para_vender: Boolean;
    Fco_ean: RawUtf8;
    Fds_observacao: RawUtf8;
    Fqt_maxima: Integer;
    Fqt_minima: Integer;
    Fco_produto: RawUtf8;
    Fds_produto: RawUtf8;
    Fid_grupo: Int64;
    Fid_grupo_empresa: Int64;
    Fid_grupo_imposto: Int64;
  published
    property id_grupo: Int64 read Fid_grupo write Fid_grupo;
    property id_grupo_empresa: Int64 read Fid_grupo_empresa write Fid_grupo_empresa;
    property co_produto: RawUtf8 read Fco_produto write Fco_produto;
    property ds_produto: RawUtf8 read Fds_produto write Fds_produto;
    property ds_descricao: RawUtf8 read Fds_descricao write Fds_descricao;
    property co_ean: RawUtf8 read Fco_ean write Fco_ean;
    property ds_unidade: RawUtf8 read Fds_unidade write Fds_unidade;
    property fl_ativo: Boolean read Ffl_ativo write Ffl_ativo;
    property fl_usa_pdv: Boolean read Ffl_usa_pdv write Ffl_usa_pdv;
    property fl_para_vender: Boolean read Ffl_para_vender write Ffl_para_vender;
    property vl_venda: Currency read Fvl_venda write Fvl_venda;
    property vl_compra: Currency read Fvl_compra write Fvl_compra;
    property fl_atualiza_compra: Boolean read Ffl_atualiza_compra write Ffl_atualiza_compra;
    property tx_atualizacao_preco: Currency read Ftx_atualizacao_preco write Ftx_atualizacao_preco;
    property qt_minima: Integer read Fqt_minima write Fqt_minima;
    property qt_maxima: Integer read Fqt_maxima write Fqt_maxima;
    property tp_material: RawUtf8 read Ftp_material write Ftp_material;
    property id_grupo_imposto: Int64 read Fid_grupo_imposto write Fid_grupo_imposto;
    property co_ncm: RawUtf8 read Fco_ncm write Fco_ncm;
    property co_cest: RawUtf8 read Fco_cest write fco_cest;
    property ds_observacao: RawUtf8 read Fds_observacao write Fds_observacao;
    property an_foto: RawUtf8 read Fan_foto write Fan_foto;
  end;
*)
  TProdutoAgille = packed record
      Cod_Produto: Integer;
      Cod_Agille: RawUtf8;
      Descricao: RawUtf8;
      CodigoBarras: RawUtf8;
      Vlr_Unitario: Double;
      Qtde: Double;
      Vlr_Desconto: Double;
      Vlr_Garcon: Double;
      Tipo_Venda: RawUtf8;
      Taxa_Garcon: RawUtf8;
      CPFCNPJ_Vendedor: RawUtf8;
      Cod_Garcon: RawUtf8;
      Nome_Garcon: RawUtf8;
      DtHora_Venda: RawUtf8;
  end;

  TParcelaAgille = packed record
      Cod_Recebimento: Integer;
      Descricao: RawUtf8;
      Valor: Double;
      DataParcelas: RawUtf8;
      NumeroParcelas: Integer;
  end;

  TVendaAgille = packed record
    Cod_Entidade: RawUtf8;
    Cod_Pedido: RawUtf8;
    DS_Origem: RawUtf8;
    DS_Parceiro: RawUtf8;
    DS_Terminal: RawUtf8;
    Cod_NF: Integer;
    Nu_NF: RawUtf8;
    Serie_NF: RawUtf8;
    Modelo_NF: RawUtf8;
    Tipo_Classificacao: Integer;
    Tipo_Classificacao_Nome: RawUtf8;
    Dt_Venda: RawUtf8;
    Vlr_TxEntrega: Double;
    Vlr_Couvert: Double;
    Vlr_DezPorCento: Double;
    Vlr_Desconto: Double;
    Valor: Double;
    status_receita_agille: Integer;
    Nome_Vendedor: RawUtf8;
    Dt_Pedido: RawUtf8;
    Cod_Cliente: Integer;
    CPFCNPJ: RawUtf8;
    Nome: RawUtf8;
    Descricao_Pedido: RawUtf8;
    Produtos: array of TProdutoAgille;
    Parcelas: array of TParcelaAgille;
    //tributos: array of TTributoItem; // (array) - Array de retorno com todos os parâmetros tributários de cada item solicitado  end;
	end;


  TfrmMain = class(TForm)
    Button1: TButton;
    DBGrid1: TDBGrid;
    dsoProdutosPDV: TDataSource;
    mtProdutosid: TLargeintField;
    mtProdutosds_produto: TStringField;
    mtProdutosds_descricao: TStringField;
    mtProdutosco_ean: TStringField;
    mtProdutosvl_venda: TCurrencyField;
    mtProdutosvl_compra: TCurrencyField;
    mtProdutosco_ncm: TStringField;
    mtProdutosco_cest: TStringField;
    mtProdutosnu_cfop: TStringField;
    mtProdutosco_cst: TStringField;
    mtProdutostx_icms_padrao: TCurrencyField;
    mtProdutos: TFDMemTable;
    Button2: TButton;
    Button3: TButton;
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure Button3Click(Sender: TObject);
  private
    { Private declarations }
    FClient: TRestHttpClient;
    FModel: TSqlModel;
    function ProcessarNotaFiscal(const AVendaAgille: TVendaAgille): TOrmNotaFiscal;
    procedure ProcessarItensNotaFiscal(const AVendaAgille: TVendaAgille;
      ANotaFiscal: TOrmNotaFiscal);
    procedure ProcessarParcelasNotaFiscal(const AVendaAgille: TVendaAgille);
    procedure GravarNotaFiscal(const AVendaAgille: TVendaAgille);

  public
    { Public declarations }
  end;

  const
  __TProdutoAgille = 'Cod_Produto: Integer; Cod_Agille: RawUtf8; Descricao: RawUtf8; CodigoBarras: RawUtf8; Vlr_Unitario: Double; '
                   + 'Qtde: Double; Vlr_Desconto: Double; Vlr_Garcon: Double; Tipo_Venda: RawUtf8; Taxa_Garcon: RawUtf8; CPFCNPJ_Vendedor: RawUtf8; '
                   + 'Cod_Garcon: RawUtf8; Nome_Garcon: RawUtf8; DtHora_Venda: RawUtf8;';

  __TVendaAgille = 'Cod_Entidade: RawUtf8; Cod_Pedido: RawUtf8; DS_Origem: RawUtf8; DS_Parceiro: RawUtf8; DS_Terminal: RawUtf8; Cod_NF: Integer; '
           + 'Nu_NF: RawUtf8; Serie_NF: RawUtf8; Modelo_NF: RawUtf8; Tipo_Classificacao: Integer; Tipo_Classificacao_Nome: RawUtf8; Dt_Venda: RawUtf8; '
           + 'Vlr_TxEntrega: Double; Vlr_Couvert: Double; Vlr_DezPorCento: Double; Vlr_Desconto: Double; Valor: Double; status_receita_agille: Integer; '
           + 'Nome_Vendedor: RawUtf8; Dt_Pedido: RawUtf8; Cod_Cliente: Integer; CPFCNPJ: RawUtf8; Nome: RawUtf8; Descricao_Pedido: RawUtf8; '
           + 'Produtos: array of TProdutoAgille; Parcelas: array of TParcelaAgille; ';
		   __ParcelaAgille = 'Cod_Recebimento: Integer; Descricao: RawUtf8; Valor: Double; DataParcelas: RawUtf8; NumeroParcelas: Integer; ';
		   var
  frmMain: TfrmMain;
  JsonAgille: RawUtf8;

implementation
uses
  RestModel,
  EmpresaOrm, GrupoEmpresaOrm, ClienteOrm, ItemNotaFiscalOrm,
  ProdutoOrm, MoviFinanceiroOrm, FormaFinanceiraOrm,
  helper.ormref;
{$R *.dfm}

procedure TfrmMain.Button1Click(Sender: TObject);
var
  TableProduto: TOrmTable;
  NomeCampo, SqlSelect: string;
  flagPDV,IdGrupoEmpresa: Integer;
begin



  if FClient.SetUser('cmarcony', 'synopse') then
  begin
    mtProdutos.Active := false;
    mtProdutos.Active := true;

    SqlSelect := 'SELECT produto.RowID id, ds_produto, produto.ds_descricao, co_ean, co_ncm, '
      + 'tx_icms_padrao, co_cest, vl_venda, vl_compra, nu_cfop, co_cst '
      + 'FROM produto '
      + 'LEFT JOIN grupoImposto ON grupoimposto.RowID = produto.id_grupo_imposto '
      + 'LEFT JOIN cfop ON cfop.RowID = grupoimposto.id_cfop '
      + 'LEFT JOIN cst ON cst.RowID  = grupoimposto.id_cst '
      + 'WHERE fl_usa_pdv = ? and produto.id_grupo_empresa = ? ';

    flagPDV := 1;
    IdGrupoEmpresa := 3;

    TableProduto := FClient.ExecuteList([], FormatSql(SqlSelect, [], [flagPDV, IdGrupoEmpresa]));
    try
      while TableProduto.Step do
      begin
        mtProdutos.Insert;

        mtProdutos.FieldByName('id').AsInteger := TableProduto.FieldAsInteger('id');

        mtProdutos.FieldByName('ds_produto').AsString := TableProduto.FieldAsString('ds_produto');
        mtProdutos.FieldByName('ds_descricao').AsString := TableProduto.FieldAsString('ds_descricao');
        mtProdutos.FieldByName('co_ean').AsString := TableProduto.FieldAsString('co_ean');
        mtProdutos.FieldByName('co_ncm').AsString := TableProduto.FieldAsString('co_ncm');
        mtProdutos.FieldByName('co_cest').AsString := TableProduto.FieldAsString('co_cest');

        mtProdutos.FieldByName('vl_venda').AsFloat := TableProduto.FieldAsFloat('vl_venda');
        mtProdutos.FieldByName('vl_compra').AsFloat := TableProduto.FieldAsFloat('vl_compra');

        mtProdutos.FieldByName('nu_cfop').AsString := TableProduto.FieldAsString('nu_cfop');
        mtProdutos.FieldByName('co_cst').AsString := TableProduto.FieldAsString('co_cst');

        mtProdutos.FieldByName('tx_icms_padrao').AsFloat := TableProduto.FieldAsFloat('tx_icms_padrao');

        mtProdutos.Post;
      end;
    finally
      TableProduto.Free;
    end;
  end;

end;

procedure TfrmMain.Button2Click(Sender: TObject);
var
  Content: RawByteString;
  VendaAgille: TVendaAgille;
begin
  Content := StringFromFile('..\..\venda-agille.json');
  RecordLoadJsonInPlace(VendaAgille, pointer(Content), TypeInfo(TVendaAgille));

  GravarNotaFiscal(VendaAgille);
end;

procedure TfrmMain.Button3Click(Sender: TObject);
begin
  FModel := DataModel;

  FClient := TRestHttpClient.Create('notei5', '8888',  FModel);
end;

procedure TfrmMain.GravarNotaFiscal(const AVendaAgille: TVendaAgille);
var
  NotaFiscal: TOrmNotaFiscal;
begin

  NotaFiscal := nil;
  FClient.Orm.TransactionBegin(TOrmNotaFiscal);
  try
    try
      NotaFiscal := ProcessarNotaFiscal(AVendaAgille);
      ProcessarItensNotaFiscal(AVendaAgille, NotaFiscal);
      ProcessarParcelasNotaFiscal(AVendaAgille);
      FClient.Orm.Commit;
    except
      FClient.Orm.RollBack;
      raise;
    end;
  finally
    NotaFiscal.Free;
  end;
end;

procedure TfrmMain.ProcessarItensNotaFiscal(const AVendaAgille: TVendaAgille;
  ANotaFiscal: TOrmNotaFiscal);
var
  Item: TOrmItemNotaFiscal;
  ProdutoAgille: TProdutoAgille;
  oProduto: TOrmProduto;
  ProdutoAF: IAutoFree;
  RestOrm: IRestOrm;
begin
  for ProdutoAgille in AVendaAgille.Produtos do
  begin
    oProduto := TOrmRefHelper.Ref<TOrmProduto>(ProdutoAgille.Cod_Produto, ProdutoAF );
    Item := TOrmItemNotaFiscal.Create;

    try
      Item.ds_produto := ProdutoAgille.Descricao;
      Item.id_nota_fiscal := ANotaFiscal.AsTOrm;
      Item.vl_unitario := ProdutoAgille.Vlr_Unitario;
      Item.qt_movimento := ProdutoAgille.Qtde;
      item.vl_desconto := ProdutoAgille.Vlr_Desconto;
      item.dt_movimento := StrToDateTime(ProdutoAgille.DtHora_Venda);
      Item.tp_movimento := 'S';
      Item.qt_movimento := ProdutoAgille.Qtde;

      FClient.Orm.Add(Item, True);
    finally
      Item.Free;
    end;
  end;

end;

function TfrmMain.ProcessarNotaFiscal(const AVendaAgille: TVendaAgille): TOrmNotaFiscal;
var
  NotaFiscal: TOrmNotaFiscal;

  oEmpresa: TOrmEmpresa;
  oGrupoEmpresa: TOrmGrupoEmpresa;
  oClient: TOrmCliente;

  EmpresaAF, GrupoEmpresaAF, ClienteAF: IAutoFree;
begin
  NotaFiscal := TOrmNotaFiscal.Create;

  oEmpresa      := TOrmRefHelper.Ref<TOrmEmpresa>(2, EmpresaAF);
  oGrupoEmpresa := TOrmRefHelper.Ref<TOrmGrupoEmpresa>(2, GrupoEmpresaAF);
  oClient       := TOrmRefHelper.Ref<TOrmCliente>(AVendaAgille.Cod_Cliente, ClienteAF);

  //AVendaAgille.Cod_Entidade
  //AVendaAgille.Cod_Pedido

  NotaFiscal.id_grupo_empresa := oGrupoEmpresa.AsTOrm;
  NotaFiscal.id_empresa       := oEmpresa.AsTOrm;
  NotaFiscal.id_cliente       := oClient.AsTOrm;

  NotaFiscal.tp_nota := 'S';
  NotaFiscal.nu_serie := AVendaAgille.Serie_NF;
  NotaFiscal.nu_modelo := AVendaAgille.Modelo_NF;
  NotaFiscal.nu_nota := Utf8ToInteger(AVendaAgille.Nu_NF);
  //AVendaAgille.Tipo_Classificacao
  //AVendaAgille.Tipo_Classificacao_Nome
  NotaFiscal.dt_entrada_saida := StrToDate(AVendaAgille.Dt_Venda); // StrToDate(
  //AVendaAgille.Vlr_TxEntrega
  //AVendaAgille.Vlr_Couvert
  NotaFiscal.vl_desconto := AVendaAgille.Vlr_Desconto;
  NotaFiscal.vl_nota := AVendaAgille.Valor;
  //AVendaAgille.status_receita_agille
  //AVendaAgille.Nome_Vendedor
  //AVendaAgille.CPFCNPJ
  //AVendaAgille.Nome
  NotaFiscal.ds_observacao := AVendaAgille.Descricao_Pedido;

  FClient.Orm.Add(NotaFiscal, True);

  Result := NotaFiscal;

end;

procedure TfrmMain.ProcessarParcelasNotaFiscal(
  const AVendaAgille: TVendaAgille);
var
  Financeiro: TOrmMoviFinanceiro;
  oFormaFinanceira: TOrmFormaFinanceira;
  FormaFinanceiraAF: IAutoFree;
begin
  for var Parcela in AVendaAgille.Parcelas do
  begin
    Financeiro := TOrmMoviFinanceiro.Create;

    try
      oFormaFinanceira      := TOrmRefHelper.Ref<TOrmFormaFinanceira>(Parcela.Cod_Recebimento, FormaFinanceiraAF);

      Financeiro.id_formaFinanceira := oFormaFinanceira.AsTOrm;
      Financeiro.vl_movimento := Parcela.Valor;
      Financeiro.nu_parcela := Parcela.NumeroParcelas;
      Financeiro.ds_historico := Parcela.Descricao;

      Financeiro.dt_movimento := StrToDate(Parcela.DataParcelas);
      FClient.Orm.Add(Financeiro, True);
    finally
      Financeiro.Free;
    end;

  end;
  //Siafw -> sem coisas da reforma


end;

initialization
//    __TRevisaoRetorno).Options := [soReadIgnoreUnknownFields, soWriteIgnoreDefault, soWriteHumanReadable]; //, soWriteHumanReadable];

  TRttiJson.RegisterFromText(TypeInfo(TProdutoAgille), __TProdutoAgille, [jpoIgnoreUnknownProperty], [woHumanReadable]);

  TRttiJson.RegisterFromText(TypeInfo(TVendaAgille)  , __TVendaAgille  , [jpoIgnoreUnknownProperty], [woHumanReadable]);

  TRttiJson.RegisterFromText(TypeInfo(TParcelaAgille), __ParcelaAgille , [jpoIgnoreUnknownProperty], [woHumanReadable]);
end.
