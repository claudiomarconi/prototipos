program ConsumoApiAgilleControl;

uses
  Vcl.Forms,
  MainForm in 'MainForm.pas' {frmMain},
  Agille.Types in '..\..\AgilleControl\src\common\Agille.Types.pas',
  helper.ormref in '..\..\AgilleControl\src\common\helper.ormref.pas',
  RestModel in '..\..\AgilleControl\src\RestModel.pas',
  BaseOrm in '..\..\AgilleControl\src\Models\BaseOrm.pas',
  CestOrm in '..\..\AgilleControl\src\Models\CestOrm.pas',
  CfopOrm in '..\..\AgilleControl\src\Models\CfopOrm.pas',
  ClienteOrm in '..\..\AgilleControl\src\Models\ClienteOrm.pas',
  ContaBancariaOrm in '..\..\AgilleControl\src\Models\ContaBancariaOrm.pas',
  ContaCorrenteOrm in '..\..\AgilleControl\src\Models\ContaCorrenteOrm.pas',
  CstBeneficioOrm in '..\..\AgilleControl\src\Models\CstBeneficioOrm.pas',
  CstOrm in '..\..\AgilleControl\src\Models\CstOrm.pas',
  DocumentoBaseOrm in '..\..\AgilleControl\src\Models\DocumentoBaseOrm.pas',
  DominioOrm in '..\..\AgilleControl\src\Models\DominioOrm.pas',
  DuplicataOrm in '..\..\AgilleControl\src\Models\DuplicataOrm.pas',
  EmpresaOrm in '..\..\AgilleControl\src\Models\EmpresaOrm.pas',
  EstoqueOrm in '..\..\AgilleControl\src\Models\EstoqueOrm.pas',
  FormaFinanceiraOrm in '..\..\AgilleControl\src\Models\FormaFinanceiraOrm.pas',
  FornecedorOrm in '..\..\AgilleControl\src\Models\FornecedorOrm.pas',
  GrupoEmpresaOrm in '..\..\AgilleControl\src\Models\GrupoEmpresaOrm.pas',
  GrupoImpostoOrm in '..\..\AgilleControl\src\Models\GrupoImpostoOrm.pas',
  GrupoOrm in '..\..\AgilleControl\src\Models\GrupoOrm.pas',
  IbptOrm in '..\..\AgilleControl\src\Models\IbptOrm.pas',
  IcmsEstadoOrm in '..\..\AgilleControl\src\Models\IcmsEstadoOrm.pas',
  ItemNotaFiscalOrm in '..\..\AgilleControl\src\Models\ItemNotaFiscalOrm.pas',
  ItemOrm in '..\..\AgilleControl\src\Models\ItemOrm.pas',
  MoviFinanceiroOrm in '..\..\AgilleControl\src\Models\MoviFinanceiroOrm.pas',
  MovimentoEstoqueOrm in '..\..\AgilleControl\src\Models\MovimentoEstoqueOrm.pas',
  NcmOrm in '..\..\AgilleControl\src\Models\NcmOrm.pas',
  NotaFiscalOrm in '..\..\AgilleControl\src\Models\NotaFiscalOrm.pas',
  NotaOficinaOrm in '..\..\AgilleControl\src\Models\NotaOficinaOrm.pas',
  NotaRestauranteOrm in '..\..\AgilleControl\src\Models\NotaRestauranteOrm.pas',
  PlanoContaOrm in '..\..\AgilleControl\src\Models\PlanoContaOrm.pas',
  PrefeituraOrm in '..\..\AgilleControl\src\Models\PrefeituraOrm.pas',
  ProdutoOrm in '..\..\AgilleControl\src\Models\ProdutoOrm.pas',
  Role in '..\..\AgilleControl\src\Models\Role.pas',
  SequencialOrm in '..\..\AgilleControl\src\Models\SequencialOrm.pas',
  TipoBaixaEstoqueOrm in '..\..\AgilleControl\src\Models\TipoBaixaEstoqueOrm.pas',
  TransportadoraOrm in '..\..\AgilleControl\src\Models\TransportadoraOrm.pas',
  UsuarioEmpresaOrm in '..\..\AgilleControl\src\Models\UsuarioEmpresaOrm.pas',
  UsuarioOrm in '..\..\AgilleControl\src\Models\UsuarioOrm.pas',
  VeiculoOrm in '..\..\AgilleControl\src\Models\VeiculoOrm.pas';

{$R *.res}

begin
  Application.Initialize;
  Application.MainFormOnTaskbar := True;
  Application.CreateForm(TfrmMain, frmMain);
  Application.Run;
end.
