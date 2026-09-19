import pandas as pd
from load import load_data


def test_load_data_creates_directory_and_file(tmp_path):
    df = pd.DataFrame({
        "cotacaoCompra": [3228.0, 5.343],
        "cotacaoVenda": [3244.0, 5.3436],
        "dataHoraCotacao": pd.to_datetime(["1985-01-07 16:45:00", "2023-01-02 13:05:57"]),
        "regime": ["administrado", "PTAX"],
        "currency": ["cruzeiro", "real"],
        "value_brl_compra": [1.173818e-09, 5.343],
        "value_brl_venda": [1.179636e-09, 5.3436],
    })

    path = tmp_path / "processed" / "processed.parquet"

    load_data(df, path=str(path))

    assert path.exists()


def test_load_data_content_matches(tmp_path):
    df = pd.DataFrame({
        "cotacaoCompra": [100.0, 200.0],
        "cotacaoVenda": [101.0, 201.0],
        "dataHoraCotacao": pd.to_datetime(["2020-01-01", "2020-01-02"]),
        "regime": ["PTAX", "PTAX"],
        "currency": ["real", "real"],
        "value_brl_compra": [100.0, 200.0],
        "value_brl_venda": [101.0, 201.0],
    })

    path = tmp_path / "processed.parquet"
    load_data(df, path=str(path))

    df_lido = pd.read_parquet(path)

    pd.testing.assert_frame_equal(df, df_lido)


def test_load_data_does_not_save_index_as_column(tmp_path):
    df = pd.DataFrame({
        "cotacaoCompra": [100.0, 200.0, 300.0],
    }, index=[5, 10, 15])  # índice "com buracos", simulando o pós-filtro do Transform

    path = tmp_path / "processed.parquet"
    load_data(df, path=str(path))

    df_lido = pd.read_parquet(path)

    assert "index" not in df_lido.columns
    assert list(df_lido.index) == [0, 1, 2]  # confirma que o índice antigo não foi salvo