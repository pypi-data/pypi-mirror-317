class BollingerBands:
    @staticmethod
    def calculate(df, window=20):
        if len(df) < window:
            raise ValueError(f"Se requieren al menos {window} datos para calcular las Bandas de Bollinger.")
        df['EMA20'] = df['Close'].rolling(window=window).mean()
        df['Bol_Up'] = df['EMA20'] + df['Close'].rolling(window=window).std() * 2
        df['Bol_Down'] = df['EMA20'] - df['Close'].rolling(window=window).std() * 2


    @staticmethod
    def generate_signals(df):
        df['Signal'] = None
        for i in range(1, len(df)):
            if df['Close'].iloc[i] < df['Bol_Down'].iloc[i] and df['Close'].iloc[i - 1] >= df['Bol_Down'].iloc[i - 1]:
                df.at[i, 'Signal'] = 'Buy'
            elif df['Close'].iloc[i] > df['Bol_Up'].iloc[i] and df['Close'].iloc[i - 1] <= df['Bol_Up'].iloc[i - 1]:
                df.at[i, 'Signal'] = 'Sell'
