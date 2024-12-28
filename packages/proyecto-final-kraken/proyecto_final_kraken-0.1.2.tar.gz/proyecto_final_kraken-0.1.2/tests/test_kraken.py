import pytest
from proyecto_kraken import KrakenClient

def test_kraken_get_pairs():
    """
    Verifica que se puedan obtener los pares de monedas desde Kraken.
    """
    client = KrakenClient()
    pairs = client.get_pairs()

    # Verificar que la respuesta es un diccionario
    assert isinstance(pairs, dict), "El resultado no es un diccionario."

    # Verificar que el diccionario tiene al menos un elemento
    assert len(pairs) > 0, "No se encontraron pares de monedas."

def test_kraken_get_ohlc_data():
    """
    Verifica que se puedan obtener datos OHLC para un par de monedas válido.
    """
    client = KrakenClient()
    pair = "BTC/USD"  # Asegúrate de que este par exista en Kraken

    # Obtener datos OHLC
    ohlc_data = client.get_ohlc_data(pair)

    # Verificar que los datos no están vacíos
    assert len(ohlc_data) > 0, "Los datos OHLC están vacíos."

    # Verificar la estructura básica de cada elemento
    for item in ohlc_data:
        assert len(item) >= 6, "Los datos OHLC no tienen el formato esperado (faltan campos)."

def test_kraken_invalid_pair():
    """
    Verifica que se maneje correctamente un par de monedas inválido.
    """
    client = KrakenClient()
    invalid_pair = "INVALID/PAIR"

    # Verificar que se lanza una excepción al usar un par inválido
    with pytest.raises(Exception, match="Error al obtener datos OHLC."):
        client.get_ohlc_data(invalid_pair)
