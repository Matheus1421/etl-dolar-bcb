import pytest
import requests
from unittest.mock import patch
from extract import extract_data, save_raw_data
import json

def test_extract_success():
    fake_response = {
    "value": [
        {"cotacaoCompra": 5.343, "cotacaoVenda": 5.3436, "dataHoraCotacao": "2023-01-02 13:05:57.593"},
        {"cotacaoCompra": 5.3753, "cotacaoVenda": 5.3759, "dataHoraCotacao": "2023-01-03 13:11:19.08"},
            ]
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_response
        result = extract_data()

    assert result == fake_response['value']

def test_extract_error():
    with patch("requests.get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("Erro simulado")

        with pytest.raises(requests.exceptions.HTTPError):
            extract_data()

def test_save_raw_data(tmp_path):
    fake_data = [{"cotacaoCompra": 5.343, "cotacaoVenda": 5.3436, "dataHoraCotacao": "2023-01-02 13:05:57.593"}]
    arquivo = tmp_path / "raw.json"

    save_raw_data(fake_data, path=str(arquivo))

    assert arquivo.exists()
    with open(arquivo, "r", encoding="utf-8") as f:
        conteudo_salvo = json.load(f)
    assert conteudo_salvo == fake_data