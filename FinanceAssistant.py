import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import pandas_datareader as web
import pickle
import sys
import datetime as dt
'''portfolio={'AAPL':20,'TSLA':5,'GS':10}'''

'''with open('portfolio.pkl','wb') as f: 
    pickle.dump(portfolio,f)'''

with open('portfolio.pkl', 'rb') as f:
    portfolio = pickle.load(f)

with open("credential.pkl", 'rb') as l:
    credential = pickle.load(l)


# credential={"shubham_pandey@srmap.edu.in":"pipInstall"}


# with open("credential.pkl","wb") as l:
    # pickle.dump(credential,l)

def save_credentials():
    print()
    with open('credential.pkl', 'wb') as l:
        pickle.dump(credential, l)

        print("Your password has been changed successfully!!! ")
        print()


def change_credentials():
    print()
    id = input("Enter your id: ")
    password = input("Enter your password: ")
    if (id in credential):
        if (credential[id] == password):
            newPassword = input("Enter your newPassword: ")
            newPassword1 = input("Enter your password again: ")

            if (newPassword == newPassword1):

                credential[id] = newPassword
                save_credentials()
                print()
                log_in()
            else:
                print("new Password didn't match: ")
                print()

                choice = int(input("Still wanna change then press 1."))
                if (choice == 1):
                    change_credentials()
                else:
                    log_in()

        else:
            print("Invalid Password!!!")
            print()
            choice = int(input("Still wanna login press 1."))
            if (choice == 1):
                change_credentials()
            else:
                log_in()

    else:
        print("Invalid Id!!")

        print()
        choice = int(input("Still wanna login then press 1."))
        if (choice == 1):
            change_credentials()
        else:
            log_in()


def process_portfolio():
    while (True):
        choice = int(input("Enter \n 1. to add shares in the portfolio: \n 2. to save shares in the portfolio: \n 3. to sell share from the portfolio: \n 4. to show the portfolio: \n 5. to show portfolio worth \n 6. to show portfolio gains \n 7. to plot charts \n 8. Bye \n-->"))

        if (choice == 1):
            add_portfolio()
        elif (choice == 2):
            save_portfolio()
        elif (choice == 3):
            remove_portfolio()
        elif (choice == 4):
            show_portfolio()
        elif (choice == 5):
            portfolio_worth()
        elif (choice == 6):
            portfolio_gains()
        elif (choice == 7):
            plot_chart()
        elif (choice == 8):
            bye()
        else:
            sys.exit(0)


def log_in():
    print()
    id = input("Enter your Id: ")
    password = input("Enter your Password: ")
    print()
    if (id in credential):
        if (credential[id] == password):
            print("successFully logged in !!")
            print()
            choice = int(input(
                "Enter \n 1 to work on your portfolio \n 2 to change your password: \n--->"))
            if (choice == 1):
                process_portfolio()
            elif (choice == 2):
                change_credentials()
            else:
                print("Invalid choice")
                print()
        else:
            print("Invalid Password !!")
            print()

    else:
        print("Invalid Id ")
        print()


# print(portfolio)


def save_portfolio():
    print()
    with open('portfolio.pkl', 'wb') as f:
        pickle.dump(portfolio, f)
    print("Your portfolio has been saved")
    print()


def add_portfolio():
    print()
    ticker = input("Which stock do you want to add: ")
    amount = input("How many shares you want to add: ")
    if (ticker in portfolio.keys()):
        portfolio[ticker] += int(amount)
    else:
        portfolio[ticker] = int(amount)

    save_portfolio()
    print()


def remove_portfolio():
    print()

    ticker = input("Enter which share you want to sell: ")
    amount = int(input("Enter how many shares you want to sell: "))

    if (ticker in portfolio.keys()):
        if (amount <= portfolio[ticker]):
            portfolio[ticker] -= int(amount)
            save_portfolio()
        else:
            print("You don't have enough shares: ")
    else:
        print(f"You don't own any share of {ticker} ")
    print()


def show_portfolio():
    print()
    print("Your portfolio: ")

    for ticker in portfolio.keys():
        print(f"You own {portfolio[ticker]} share of {ticker} ")

    print()


def portfolio_worth():
    print()
    sum = 0
    for ticker in portfolio.keys():
        data = web.DataReader(ticker, 'yahoo')
        print(data)

        #price = (data['Close'].iloc[-1])*portfolio[ticker]
        #sum += price
    #print(f"Your portfolio worth is {sum} $ ")
    print()


def portfolio_gains():
    print()
    starting_date = input("Enter a date for comparison (YYYY-MM-DD): ")
    sum_now = 0
    sum_then = 0
    try:
        for ticker in portfolio.keys():
            data = web.DataReader(ticker, 'yahoo', starting_date, str(
                dt.datetime.today()).split()[0])

            price_now = (data['Close'].iloc[-1])*portfolio[ticker]
            #price_then=data.loc[data.index == starting_date]['Close'].values[0]
            price_then = data['Close'].iloc[0]*portfolio[ticker]

            sum_now += price_now
            sum_then += price_then
        print(f"Relative Gains: {((sum_now-sum_then)/sum_then)*100}% ")
        print(f"Absolute Gains: {(sum_now-sum_then )} $")
        print()
    except IndexError:
        print("There was no trading on this day ")
        print()


def plot_chart():
    print()
    ticker = input("Choose a ticker symbol: ")
    starting_string = input("Choose a starting date (DD/MM/YYYY): ")
    plt.style.use('dark_background')

    start = dt.datetime.strptime(starting_string, "%d/%m/%Y")
    end = dt.datetime.now()

    data = web.DataReader(ticker, 'yahoo', start, end)

    colors = mpf.make_marketcolors(
        up='#00ff00', down='#ff0000', wick='inherit', edge='inherit', volume='inherit') #'#00ff00'===> green ,down='#ff0000===>red
    mpf_style = mpf.make_mpf_style(
        base_mpf_style='nightclouds', marketcolors=colors)
    mpf.plot(data, type='candle', style=mpf_style, volume=True)
    print()


def bye():
    print()
    print("Good bye")
    print()
    sys.exit(0)


log_in()
