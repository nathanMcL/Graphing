# The purpose of this program:
# Using a Yahoo Finance library
# Given a Companies stock symbol
# Graph year to date stock related data

# Graph features:
# Name of Company
# Current date/time of the query
# Graph refreshes every thirty seconds, retrieving updated data *I think :)

# Toggle off/on legend features:
# Stock symbol
# Current price of the query

# ***Not certain if the refresh is updating the current stock price and reflecting on the graph

import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from datetime import datetime, timedelta
from matplotlib.animation import FuncAnimation

# Global variables to store line objects and stock data
lines = {}
annotations = {}
stock_data_store = {}
show_current_price = {'enabled': True}


def update_data(frame):
    global lines, annotations, ax

    for ticker, _ in lines.items():
        for line in lines[ticker]:
            line.remove()

    if show_current_price['enabled']:
        for annotation in annotations.values():
            annotation.remove()

    lines.clear()
    annotations.clear()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    plot_stock_data(ax, 'AAPL', start_date_str, end_date_str, 'g', 'r')

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ax.annotate(f"Current Time: {current_time}", xy=(0.01, 0.98), xycoords="axes fraction", ha='left', va='top')

    plt.draw()


def plot_stock_data(ax, ticker_symbol, start_date, end_date, color_up, color_down):
    global lines, annotations

    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    stock_data_store[ticker_symbol] = stock_data

    dates = stock_data.index
    close_prices = stock_data['Close']

    prev_price = close_prices[0]
    prev_date = dates[0]
    line_segments = []

    for date, price in zip(dates[1:], close_prices[1:]):
        if price > prev_price:
            line, = ax.plot([prev_date, date], [prev_price, price], color=color_up)
        else:
            line, = ax.plot([prev_date, date], [prev_price, price], color=color_down)

        line_segments.append(line)
        prev_date, prev_price = date, price

    lines[ticker_symbol] = line_segments

    if show_current_price['enabled']:
        annotation = ax.annotate(
            f'Current Price: ${close_prices[-1]}',
            xy=(dates[-1], close_prices[-1]),
            textcoords="offset points",
            xytext=(0, 10),
            ha='center'
        )
        annotations[ticker_symbol] = annotation


def toggle_lines(label):
    global annotations
    if label == 'Current Price':
        show_current_price['enabled'] = not show_current_price['enabled']
        for annotation in annotations.values():
            annotation.set_visible(show_current_price['enabled'])
    else:
        visibility = not lines[label][0].get_visible()
        for line in lines[label]:
            line.set_visible(visibility)
    plt.draw()


def on_hover(event):
    for ticker_symbol, line_segments in lines.items():
        for i, line in enumerate(line_segments):
            if line.contains(event)[0]:
                dates = stock_data_store[ticker_symbol].index
                close_prices = stock_data_store[ticker_symbol]['Close']
                date = dates[i]
                price = close_prices[i]
                tooltip.xy = (event.xdata, event.ydata)
                tooltip.set_text(f"{ticker_symbol}\nDate: {date.strftime('%Y-%m-%d')}\nPrice: ${price:.2f}")
                tooltip.set_visible(True)
                plt.draw()
                return
    tooltip.set_visible(False)
    plt.draw()


if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.2)

    ax.set_title('Apple Inc. Stock Prices')
    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price (in USD)')
    ax.set_facecolor('#a4edc3')  # Set the background color
    ax.grid(True)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    plot_stock_data(ax, 'AAPL', start_date_str, end_date_str, 'g', 'r')
    # plot_stock_data(ax, 'GOOG', start_date_str, end_date_str, 'b', 'orange')

    for annotation in annotations.values():
        annotation.set_visible(show_current_price['enabled'])

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ax.annotate(f"Current Time: {current_time}", xy=(0.01, 0.98), xycoords="axes fraction", ha='left',
                va='top')  # Add the current time

    tooltip = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(20, 20),
        textcoords="offset points",
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"),
        arrowprops=dict(arrowstyle="->")
    )
    tooltip.set_visible(False)

    # Set up FuncAnimation to refresh the graph every 30 seconds (30000 milliseconds)
    ani = FuncAnimation(fig, update_data, interval=30000, save_count=25)

    rax = plt.axes([0.05, 0.4, 0.1, 0.15])
    check = CheckButtons(rax, ('AAPL', 'Current Price'), (True, True))
    check.on_clicked(toggle_lines)

    fig.canvas.mpl_connect("motion_notify_event", on_hover)

    plt.show()
