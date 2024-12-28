import pytest
import pandas as pd
from src.proyecto_kraken.bollinger_bands import BollingerBands
from src.proyecto_kraken.plot_utils import plot_data

def test_plot_data_runs():
    """
    Verifica que la función de graficar no lanza errores con datos válidos.
    """
    # Crear datos de ejemplo
    data = {
        'Time': pd.date_range(start='2023-01-01', periods=21, freq='D'),
        'Close': [10, 12, 13, 15, 17, 20, 21, 19, 18, 17, 22, 23, 25, 24, 27, 30, 29, 28, 26, 25, 24],
        'Signal': [None] * 19 + ['Buy', 'Sell']
    }
    df = pd.DataFrame(data)

    # Calcular Bandas de Bollinger
    BollingerBands.calculate(df)

    # Intentar graficar
    try:
        plot_data(df, pair_name="BTC/USD", quote_currency="USD")
    except Exception as e:
        pytest.fail(f"La función de graficar falló con el error: {e}")
