import matplotlib.pyplot as plt

def plot_data(df, pair_name, quote_currency):
    fig, ax = plt.subplots(figsize=(12, 10))
    series = [
        ['Close', 'blue', '-'],
        ['EMA20', 'red', '--'],
        ['Bol_Up', 'orange', '-'],
        ['Bol_Down', 'orange', '-']
    ]

    for label, color, linestyle in series:
        ax.plot(df['Time'], df[label], label=label, color=color, linestyle=linestyle)

    # Añadir señales
    buy_signals = df[df['Signal'] == 'Buy']
    sell_signals = df[df['Signal'] == 'Sell']
    ax.scatter(buy_signals['Time'], buy_signals['Close'], marker='^', color='green', label='Buy Signal', s=100)
    ax.scatter(sell_signals['Time'], sell_signals['Close'], marker='v', color='red', label='Sell Signal', s=100)

    ax.set_title(f'Precios de Cierre de {pair_name}')
    ax.set_xlabel('Tiempo')
    ax.set_ylabel(f'Precio de Cierre ({quote_currency})')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
