from neuralintents import GenericAssistance
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import mplfinance as mpf

import pickle
import sys
import datetime as dt

portfolio = {'APPL': 20, 'ETH': 10, 'BTC': 30}

with open('portfolio.pkl', 'eb') as f:
    pickle.dump(portfolio, f)

with open('portfolio.pkl', 'rb') as f:
    portfolio = pickle.load(f)


def save_portifolio():
    with open('portfolio.pkl', 'wb') as f:
        pickle.dump(portfolio, f)


def add_portifolio():
    ticker = input("Which stoke do you want to add?: ")
    amount = input("How many share do you want to add?:")

    if ticker in portfolio.keys():
        portfolio[ticker] += int(amount)
    else:
        portfolio[ticker] = int(amount)

    save_portifolio()

    def remove_portfolio():
        ticker = input("Which stock do you want to sell?: ")
        amount = input("How many shares do you want to sell:")

        if ticker in portfolio.keys():
            if amount <= portfolio[ticker]:
                portfolio[ticker] -= int(amount)
                save_portifolio()
            else:
                print("You do not have enough share!")
        else:
            print(f"You own do not own any share of {ticker}")

    def show_portfolio():
        print("Your portfolio:")
        for ticker in portfolio.keys():
            print(f"You own {portfolio[ticker]} share of {ticker}")

    def portfolio_worth():
        sum = 0
        for ticker in portfolio.keys():
            data = web.DataReader(ticker, 'yahoo')
            price = data['Close'].iloc[-1]
            sum += price
        print(f"Your portfolio is worth {sum} USD")

    def portfolio_gains():
        starting_date = input("Enter a date for comparison (YY-MM-DD): ")

        sum_now = 0
        sum_then = 0

        try:
            for ticker in portfolio.keys():
                data = web.DataReader(ticker, 'yahoo')
                price_now = data['Close'].iLoc[-1]
                price_then = data.loc[data.index ==
                                      starting_date]['Close'].values[0]
                sum_now += price_now
                sum_then = price_then

            print(f"Relative Gains: {((sum_now-sum_then)/sum_then) * 100}%")
            print(f"Absolute Gains: {sum_now-sum_then} USD")
        except IndexError:
            print("There was no trading on this day!")

    def plot_chart():
        ticker = input("Choose a ticker symbol: ")
        starting_string = input("Choose a strting date (DD/MM/YYY): ")

        plt.style.use('dark_background')

        start = dt.datetime.strptime(starting_string, "%d/%m/%Y")
        end = dt.datetime.now()

        data = web.DataReader(ticker, 'yahoo', start, end)

        colors = mpf.make_marketcolors(
            up='#00ff00', down='#ff0000', wick='inherit', edge='inherit', volume='in')
        mpf_style = mpf.make_mpf_style(
            base_mpf_style='nightcloud', marketcolors=colors)
        mpf.plot(date, type='candle', style=mpf_style, volume=True)

    def bye():
        print("Goodbye")
        sys.exit(0)

    mappings = {
        'plot_chart': plot_chart,
        'add_portifolio': add_portifolio,
        'remove_portfolio': remove_portfolio,
        'show_portfolio': show_portfolio,
        'portfolio_worth': portfolio_worth,
        'portfolio_gains': portfolio_gains,
        'bye': bye
    }
    assistant = GenericAssistant(
        'intents.json', mappings, "finacial_assistant_model")

    assistant.train_model()
    assistant.save_mode()

    while True:
        message = input(" ")
        assistant.request(message)
