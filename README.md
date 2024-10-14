# PyCoin
#### Description:

This is a command line python program. It is basically a crypto exchange made in python.
I thought of this idea when I was on my phone and I saw the binance app, I thought my skills were sufficient enough and initially
I thought I could do all of this using a data base such as SQL,python and some sort of API. Initially I didn't know which API to use or how
to go about it in this scenario but I did some research and I quickly found that coingecko's and coindesk's were my best choice in this scenario.
My knowledge from using API's in my CS50X project came in very very handy and I was quickly able to figure everything out.
Overall I think this project came out very well and I incorporated most of what I learned from the CS50 python course.

One design flaw I notice in my project is that I could've incorporated classes. Though everything / most things can be done with functions at this level
of code, it would just be cleaner and implemented in a better way with classes. For example rather than having deposit_withdraw() and buy_sell() functions. I could have made classes such as manage_funds and manage_crypto. Since there is more functions being used inside them functions its not super clear to read for a different programmer.

There is quite a few functions in my program, and I tried to isolate them as much as possible, so each function does its own task.
I think in terms of reusability , I did my functions well, and the error handling is handled inside the functions for the most part
Lets go through what each function does

print_menu() Prints the menu

price_lookup() Prompts the user to look up price of cryptocurrency

deposit_withdraw() Allows user to deposit and withdraw funds to account

buy_sell() Allows user to buy and sell crypto coins to and from their wallet

price_history(coin,days) returns price history of a coin based on what coin it is and number of days back

current_price(coin) returns current price of coin

portfolio() prints all of users coins along with price

watchlist() prints users watchlist

popular() prints the top 10 coins by market cap

clear_account() deletes everything from each sql table : clears the database

get_crypto_balance(coin) gets user coin balance

get_balance(type) gets user funds balance

user_insert(type,amount,newBal) adds deposit/withdraw/buy/sell entries into users account

coins_insert(action,coin,amount,balance) adds buy/sell entries into users crypto coins holdings

watchlist_insert(coin) insterts coins and price into watchlist







