import pytest
import datetime
import pandas as pd
from transform import define_regime, define_currency, convert_to_brl, transform_data


def test_define_regime_administrado():
    data = datetime.datetime(1985, 6, 1, 12, 0, 0)
    assert define_regime(data) == "administrado"


def test_define_regime_interbancario():
    data = datetime.datetime(2000, 1, 1, 12, 0, 0)
    assert define_regime(data) == "interbancário"


def test_define_regime_ptax():
    data = datetime.datetime(2020, 1, 1, 12, 0, 0)
    assert define_regime(data) == "PTAX"


def test_define_regime_boundary_administrado_end():
    data = datetime.datetime(1990, 3, 18, 23, 59, 59)
    assert define_regime(data) == "administrado"


def test_define_regime_boundary_interbancario_start():
    data = datetime.datetime(1990, 3, 19, 0, 0, 0)
    assert define_regime(data) == "interbancário"


def test_define_regime_out_of_range_raises():
    data = datetime.datetime(1980, 1, 1)
    with pytest.raises(ValueError):
        define_regime(data)


def test_define_currency_cruzeiro_antigo():
    currency, factor = define_currency(datetime.datetime(1985, 6, 1))
    assert currency == "cruzeiro"
    assert factor == 2_750_000_000_000


def test_define_currency_real():
    currency, factor = define_currency(datetime.datetime(2020, 1, 1))
    assert currency == "real"
    assert factor == 1


def test_define_currency_out_of_range_raises():
    with pytest.raises(ValueError):
        define_currency(datetime.datetime(1980, 1, 1))


def test_convert_to_brl_with_conversion():
    assert convert_to_brl(2750, 2750) == 1.0


def test_convert_to_brl_no_conversion():
    assert convert_to_brl(5.343, 1) == 5.343


def test_transform_data_filters_and_adds_columns():
    dados = [
        {"cotacaoCompra": 100.0, "cotacaoVenda": 101.0, "dataHoraCotacao": "1984-12-01 10:00:00.0"},
        {"cotacaoCompra": 3228.0, "cotacaoVenda": 3244.0, "dataHoraCotacao": "1985-01-07 16:45:00.0"},
        {"cotacaoCompra": 5.343, "cotacaoVenda": 5.3436, "dataHoraCotacao": "2023-01-02 13:05:57.593"},
    ]

    df = transform_data(dados)

    assert len(df) == 2  # o registro de 1984 deve ser filtrado

    assert list(df.columns) == [
        "cotacaoCompra", "cotacaoVenda", "dataHoraCotacao",
        "regime", "currency", "value_brl_compra", "value_brl_venda",
    ]

    linha_1985 = df.iloc[0]
    assert linha_1985["regime"] == "administrado"
    assert linha_1985["currency"] == "cruzeiro"
    assert linha_1985["value_brl_compra"] == 3228.0 / 2_750_000_000_000

    linha_2023 = df.iloc[1]
    assert linha_2023["regime"] == "PTAX"
    assert linha_2023["currency"] == "real"
    assert linha_2023["value_brl_compra"] == 5.343