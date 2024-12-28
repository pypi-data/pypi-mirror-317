import krakenex

class KrakenClient:
    def __init__(self):
        self.api = krakenex.API()

    def get_pairs(self):
        response = self.api.query_public('AssetPairs')
        if 'error' in response and response['error']:
            raise Exception("Error al obtener pares de Kraken.")
        return response['result']

    def get_ohlc_data(self, pair, interval=60):
        response = self.api.query_public('OHLC', {'pair': pair, 'interval': interval})
        if 'error' in response and response['error']:
            raise Exception("Error al obtener datos OHLC.")
        return response['result'][pair]
