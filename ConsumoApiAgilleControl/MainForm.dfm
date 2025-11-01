object frmMain: TfrmMain
  Left = 0
  Top = 0
  Caption = 'frmMain'
  ClientHeight = 567
  ClientWidth = 1182
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  PixelsPerInch = 96
  TextHeight = 13
  object Button1: TButton
    Left = 32
    Top = 24
    Width = 75
    Height = 25
    Caption = 'Button1'
    TabOrder = 0
    OnClick = Button1Click
  end
  object DBGrid1: TDBGrid
    Left = 32
    Top = 55
    Width = 1097
    Height = 426
    DataSource = dsoProdutosPDV
    TabOrder = 1
    TitleFont.Charset = DEFAULT_CHARSET
    TitleFont.Color = clWindowText
    TitleFont.Height = -11
    TitleFont.Name = 'Tahoma'
    TitleFont.Style = []
  end
  object Button2: TButton
    Left = 160
    Top = 24
    Width = 75
    Height = 25
    Caption = 'Button2'
    TabOrder = 2
    OnClick = Button2Click
  end
  object dsoProdutosPDV: TDataSource
    DataSet = mtProdutos
    Left = 512
    Top = 192
  end
  object mtProdutos: TFDMemTable
    Active = True
    FieldDefs = <
      item
        Name = 'id'
        DataType = ftLargeint
      end
      item
        Name = 'ds_produto'
        DataType = ftString
        Size = 255
      end
      item
        Name = 'ds_descricao'
        DataType = ftString
        Size = 255
      end
      item
        Name = 'co_ean'
        DataType = ftString
        Size = 255
      end
      item
        Name = 'vl_venda'
        DataType = ftCurrency
        Precision = 19
      end
      item
        Name = 'vl_compra'
        DataType = ftCurrency
        Precision = 19
      end
      item
        Name = 'co_ncm'
        DataType = ftString
        Size = 8
      end
      item
        Name = 'co_cest'
        DataType = ftString
        Size = 8
      end
      item
        Name = 'nu_cfop'
        DataType = ftString
        Size = 4
      end
      item
        Name = 'co_cst'
        DataType = ftString
        Size = 3
      end
      item
        Name = 'tx_icms_padrao'
        DataType = ftCurrency
        Precision = 19
      end>
    IndexDefs = <>
    FetchOptions.AssignedValues = [evMode]
    FetchOptions.Mode = fmAll
    ResourceOptions.AssignedValues = [rvSilentMode]
    ResourceOptions.SilentMode = True
    UpdateOptions.AssignedValues = [uvCheckRequired, uvAutoCommitUpdates]
    UpdateOptions.CheckRequired = False
    UpdateOptions.AutoCommitUpdates = True
    StoreDefs = True
    Left = 824
    Top = 272
    object mtProdutosid: TLargeintField
      DisplayWidth = 7
      FieldName = 'id'
    end
    object mtProdutosds_produto: TStringField
      DisplayWidth = 49
      FieldName = 'ds_produto'
      Size = 255
    end
    object mtProdutosds_descricao: TStringField
      DisplayWidth = 33
      FieldName = 'ds_descricao'
      Size = 255
    end
    object mtProdutosco_ean: TStringField
      DisplayWidth = 15
      FieldName = 'co_ean'
      Size = 255
    end
    object mtProdutosvl_venda: TCurrencyField
      DisplayWidth = 10
      FieldName = 'vl_venda'
    end
    object mtProdutosvl_compra: TCurrencyField
      DisplayWidth = 10
      FieldName = 'vl_compra'
    end
    object mtProdutosco_ncm: TStringField
      DisplayWidth = 8
      FieldName = 'co_ncm'
      Size = 8
    end
    object mtProdutosco_cest: TStringField
      DisplayWidth = 8
      FieldName = 'co_cest'
      Size = 8
    end
    object mtProdutosnu_cfop: TStringField
      DisplayWidth = 6
      FieldName = 'nu_cfop'
      Size = 4
    end
    object mtProdutosco_cst: TStringField
      DisplayWidth = 5
      FieldName = 'co_cst'
      Size = 3
    end
    object mtProdutostx_icms_padrao: TCurrencyField
      DisplayWidth = 12
      FieldName = 'tx_icms_padrao'
    end
  end
end
