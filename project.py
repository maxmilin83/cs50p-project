import requests
import sqlite3
import sys


#SQLITE Setup

conn = sqlite3.connect("data.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY,action TEXT,amount INTEGER,balance INTEGER);")
cur.execute("CREATE TABLE IF NOT EXISTS coins (id INTEGER PRIMARY KEY,action TEXT,coin TEXT,amount INTEGER,balance INTEGER);")
cur.execute("CREATE TABLE IF NOT EXISTS watchlist(id INTEGER PRIMARY KEY,coin TEXT unique,price INTEGER);")

#Main function
def main():
    while True:

        if len(sys.argv) != 2:
            print("Invalid usage")
            break
        if sys.argv[1].lower() != "start":
            print("Invalid usage")
            break

        print_menu()
        try:
            user = int(input("Select option 1-7: "))
        except (ValueError,UnboundLocalError):
            input("Invalid usage press to continue...")
            continue

        match user:
            case 1:
                price_lookup()
            case 2:
                deposit_withdraw()
            case 3:
                buy_sell()
            case 4:
                portfolio()
                input("Press to go back...")
            case 5:
                watchlist()
            case 6:
                popular()
                input("Press to go back...")
            case 7:
                clear_account()
            case _:
                input("Invalid usage press to continue...")


def print_menu():
    print("-----------------")
    print("1. Price Lookup ")
    print("2. Deposit/Withdraw funds")
    print("3. Buy/Sell Crypto")
    print("4. Portfolio")
    print("5. Watchlist")
    print("6. Popular Cryptocurrencies")
    print("7. Clear Account")

def price_lookup():
    while True:

        coin = input("Enter cryptocurrency: ")
        coin = coin.lower()
        if current_price(coin) == "Invalid":
            print("Invalid cryptocurrency / too many requests")
            continue

        while True:
            try:
                dayz = int(input("Enter price history in days: "))
            except ValueError:
                print("Enter number of days")
                continue
            for i in range(dayz):

                if i == 0:
                    print("Today: \t   "+ current_price(coin))
                try:
                    print(i+1,"day ago:",price_history(coin,i))

                except KeyError:
                    continue
            break
        break
    input("Press to continue...")

def deposit_withdraw():

    balance = get_balance("user")
    conn.commit()

    print("----------------")
    print("Current balance:"+ f" ${balance}")
    print("----------------")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Back")
    select = int(input(""))
    match select:
        case 1:
            while True:
                try:
                    amount=int(input("Amount to deposit (USD): "))
                except ValueError:
                    print("Must enter amount in USD")
                    continue

                user_insert('deposit',amount,(amount+balance))
                conn.commit()
                input("Success! press to continue...")
                break

        case 2:
            while True:
                try:
                    amount=int(input("Amount to withdraw (USD): "))
                except ValueError:
                    print("Must enter amount in USD")
                    continue


                total = balance-amount

                if amount <= 0 or total <= 0:
                    print("Can't withdraw this amount")
                    return 1

                user_insert('withdraw',amount,(balance-amount))
                conn.commit()
                input("Success! press to continue...")
                break
        case 3:
            return 1


def buy_sell():
    print("--------------")
    print("1.Buy crypto")
    print("2.Sell crypto")
    print("3.Back")
    user = int(input(""))
    match user:
        case 1:
            while True:
                balance = get_balance("user")
                if balance <= 0:
                    input("Insufficient funds... Press to go back...")
                    break

                user = input("Search crypto: ")
                if current_price(user) == "Invalid":
                    print("Invalid cryptocurrency")
                    continue
                print("Current price: ",current_price(user),"per 1",user)
                while True:
                    try:
                        amount = int(input("Amount to buy: (USD): "))
                        if amount<0:
                            print("Enter valid amount")
                            continue
                        if amount>=balance:
                            print("Insufficient funds")
                            continue
                        input("Success! press to continue...")
                        break
                    except ValueError:
                        print("Enter valid amount")
                        continue

                crypto_balance = get_crypto_balance(user)
                coins_insert('buy',user,amount,(crypto_balance+amount))
                conn.commit()
                user_insert('buy',amount,balance-amount)
                conn.commit()
                break

        case 2:
            while True:
                balance = get_balance("user")
                user = input("Search crypto: ")
                if current_price(user) == "Invalid":
                        print("Invalid cryptocurrency")
                        continue

                print("Current price: ",current_price(user),"per 1",user)

                print(user.title(),"balance: "+f"${get_crypto_balance(user)}")
                crypto_balance = get_crypto_balance(user)
                if crypto_balance <= 0:
                    input("Press to go back... ")
                    break
                while True:
                    try:
                        amount = int(input("Amount to sell: (USD): "))
                        if amount<0:
                            print("Enter valid amount")
                            continue
                        if amount>crypto_balance:
                            print("Amount greater than balance")
                            continue

                        input("Success! press to continue...")
                        break

                    except ValueError:
                        print("Enter valid amount")
                        continue


                coins_insert('sell',user,amount,(crypto_balance-amount))
                conn.commit()
                user_insert('sell',amount,balance+amount)
                break

        case 3:
            return 1


def price_history(coin,days):
    string = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days={days}&interval=daily"
    request = requests.get(string,headers = {"accept":"application/json"})
    price = request.json()
    price = round(price["prices"][0][1])

    try:
        return f"${price}"
    except KeyError:
        return f"{request}"

def current_price(coin):
    string = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    request = requests.get(string,headers = {"accept":"application/json"})
    price = request.json()
    try:
        return f"${price[(coin)]['usd']}"
    except KeyError:
        return f"Invalid"

def portfolio():
    coins = cur.execute("SELECT DISTINCT coin FROM coins;")
    coins = coins.fetchall()

    coinsList = {}

    for coin in coins:
        coinsList[coin[0]] = 0

    for coin in coinsList:
        coinsList[coin] = get_crypto_balance(coin)

    if coinsList:
        print("Portfolio")
        print("--------------------")
        for coin,price in coinsList.items():
            print(f"{coin.title()}: ${price}")
        print("--------------------")

    if not coinsList:
        print("Empty portfolio")
        print("--------------------")

def watchlist():

    watchlist = cur.execute("SELECT coin,price FROM watchlist;")
    watchlist = watchlist.fetchall()

    if not watchlist:
        print("Empty watchlist")


    if watchlist:
        print("Current watchlist: ")
        print("--------------------")


    for coin,price in watchlist:
        print(f"{coin.title()}: {price}")

    print("--------------------")
    print("1. Add to watchlist")
    print("2. Back")
    user = int(input(""))
    match user:
        case 1:
            while True:
                try:
                    add = input("Enter crypto currency: ")

                    if current_price(add) == "Invalid":
                        print("Invalid cryptocurrency")
                        continue

                    watchlist_insert(add)
                    conn.commit()
                    input("Success! press to continue...")
                except sqlite3.IntegrityError:
                    print("Already in watchlist")
                    continue
                break
        case 2:
            return 1

def popular():
    string = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false&locale=en"
    request = requests.get(string,headers = {"accept":"application/json"})
    request = request.json()

    for i in range(10):
        print(f"{request[i]['id'].title()}: ${request[i]['current_price']}")


def clear_account():
    user=input("Are you sure you want to clear account? (Y/N): ")

    if user.lower() == "y":

        cur.execute("DELETE FROM user;")
        conn.commit()
        cur.execute("DELETE FROM coins;")
        conn.commit()
        cur.execute("DELETE FROM watchlist;")
        conn.commit()
        print("Account cleared...")
        input("Press to continue... ")




## actions
def get_crypto_balance(coin):
    try:
        bal = cur.execute("SELECT balance FROM coins WHERE coin = ? ORDER BY id DESC;",(coin,))
        bal = bal.fetchone()[0]
        return bal
    except TypeError:
        return 0

def get_balance(type):
    string = f"SELECT balance FROM {type} ORDER BY id DESC;"
    try:
        bal = cur.execute(string)
        return bal.fetchone()[0]
    except TypeError:
        return 0

def user_insert(type,amount,newBal):
    return cur.execute("INSERT INTO user (action,amount,balance) VALUES (?,?,?);",(type,amount,(newBal)))

def coins_insert(action,coin,amount,balance):
    return cur.execute("INSERT INTO coins (action,coin,amount,balance) VALUES (?,?,?,?);",(action,coin,amount,balance))

def watchlist_insert(coin):
    price = current_price(coin)
    return cur.execute("INSERT INTO watchlist (coin,price) VALUES (?,?);",(coin,price))


if __name__ == "__main__":
    main()