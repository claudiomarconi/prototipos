program ConsumoApiAgilleControl;

uses
  Vcl.Forms,
  MainForm in 'MainForm.pas' {frmMain},
  BaseOrm in 'C:\Desenv\AgilleControl\src\Models\BaseOrm.pas',
  ClienteOrm in 'C:\Desenv\AgilleControl\src\Models\ClienteOrm.pas',
  EmpresaOrm in 'C:\Desenv\AgilleControl\src\Models\EmpresaOrm.pas',
  FornecedorOrm in 'C:\Desenv\AgilleControl\src\Models\FornecedorOrm.pas',
  GrupoEmpresaOrm in 'C:\Desenv\AgilleControl\src\Models\GrupoEmpresaOrm.pas',
  TipoBaixaEstoqueOrm in 'C:\Desenv\AgilleControl\src\Models\TipoBaixaEstoqueOrm.pas',
  TransportadoraOrm in 'C:\Desenv\AgilleControl\src\Models\TransportadoraOrm.pas',
  NotaFiscalOrm in 'C:\Desenv\AgilleControl\src\Models\NotaFiscalOrm.pas',
  PrefeituraOrm in 'C:\Desenv\AgilleControl\src\Models\PrefeituraOrm.pas',
  Agille.Types in 'C:\Desenv\AgilleControl\src\common\Agille.Types.pas',
  helper.ormref in 'C:\Desenv\AgilleControl\src\common\helper.ormref.pas',
  ItemNotaFiscalOrm in 'C:\Desenv\AgilleControl\src\Models\ItemNotaFiscalOrm.pas',
  ProdutoOrm in 'C:\Desenv\AgilleControl\src\Models\ProdutoOrm.pas',
  GrupoImpostoOrm in 'C:\Desenv\AgilleControl\src\Models\GrupoImpostoOrm.pas',
  CfopOrm in 'C:\Desenv\AgilleControl\src\Models\CfopOrm.pas',
  CstOrm in 'C:\Desenv\AgilleControl\src\Models\CstOrm.pas',
  GrupoOrm in 'C:\Desenv\AgilleControl\src\Models\GrupoOrm.pas';

{$R *.res}

begin
  Application.Initialize;
  Application.MainFormOnTaskbar := True;
  Application.CreateForm(TfrmMain, frmMain);
  Application.Run;
end.
