from src.proyecto_kraken.kraken_client import KrakenClient
from src.proyecto_kraken.bollinger_bands import BollingerBands
from src.proyecto_kraken.plot_utils import plot_data
import pandas as pd

def main():
    # Instanciar cliente de Kraken
    kraken = KrakenClient()
    pairs = kraken.get_pairs()
    pair_list = list(pairs.keys())

    # Selección del par
    for i, pair in enumerate(pair_list):
        print(f"{i}. {pair}")
    while True:
        try:
            selected_index = int(input("Seleccione el número correspondiente al par de monedas: "))
            selected_pair = pair_list[selected_index]
            break
        except (ValueError, IndexError):
            print("Favor seleccione un número válido.")

    # Obtener datos
    ohlc_data = kraken.get_ohlc_data(selected_pair)
    timestamps = [pd.to_datetime(item[0], unit='s') for item in ohlc_data]
    close_prices = [float(item[4]) for item in ohlc_data]

    # Crear DataFrame
    df = pd.DataFrame({'Time': timestamps, 'Close': close_prices})
    BollingerBands.calculate(df)
    BollingerBands.generate_signals(df)

    # Información del par
    pair_info = pairs[selected_pair]
    pair_name = pair_info['wsname']
    quote_currency = pair_name.split('/')[1]

    # Graficar
    plot_data(df, pair_name, quote_currency)


if __name__ == "__main__":
    main()
