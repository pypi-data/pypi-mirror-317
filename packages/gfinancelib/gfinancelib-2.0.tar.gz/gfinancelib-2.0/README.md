# Financial Analysis Library

## Created by: Francesco Vito Giotta (LemonPower21)

This library was created by Francesco Vito Giotta to provide a set of tools for financial analysis using Python. It leverages the `yfinance` and `ta` libraries for retrieving stock data, calculating technical indicators, and sending email notifications.

## Overview
This library provides a set of functions for financial analysis using the `yfinance` and `ta` libraries. It includes functionalities for retrieving stock prices, calculating financial indicators, and sending notifications.

## Functions

### `bid(ticker)`
Fetches the bid price of the specified stock ticker.

- **Parameters:**
  - `ticker` (str): The ticker symbol of the stock.
- **Returns:**
  - `float`: The bid price, or `0` if not available.

### `ask(ticker)`
Fetches the ask price of the specified stock ticker.

- **Parameters:**
  - `ticker` (str): The ticker symbol of the stock.
- **Returns:**
  - `float`: The ask price, or `0` if not available.

### `start()`
Starts a timer to track elapsed time.

- **Returns:**
  - `float`: The start time (epoch timestamp).

### `stop(start)`
Stops the timer and calculates the elapsed time from the start.

- **Parameters:**
  - `start` (float): The start time returned by the `start()` function.
- **Returns:**
  - `tuple`: The elapsed time in years, months, days, hours, minutes, and seconds.

### `log(text)`
Logs a message to a log file and waits for network connectivity before doing so.

- **Parameters:**
  - `text` (str): The message to log.
- **Returns:** 
  - `None`

### `last(ticker)`
Fetches the last closing price for the specified ticker.

- **Parameters:**
  - `ticker` (str): The ticker symbol of the stock.
- **Returns:**
  - `float`: The last closing price, or `None` if an error occurs.

### `rsi(ticker, periods, chart, timeframe)`
Calculates the Relative Strength Index (RSI) for the specified ticker.

- **Parameters:**
  - `ticker` (str): The ticker symbol of the stock.
  - `periods` (int): The number of periods for the RSI calculation.
  - `chart` (str): The chart period (e.g., "1y", "6mo").
  - `timeframe` (str): The time interval (e.g., "1m", "5m").
- **Returns:**
  - `float`: The RSI value, or `None` if an error occurs.

### `ema(ticker, periods, chart, timeframe)`
Calculates the Exponential Moving Average (EMA) for the specified ticker.

- **Parameters:**
  - `ticker` (str): The ticker symbol of the stock.
  - `periods` (int): The number of periods for the EMA calculation.
  - `chart` (str): The chart period (e.g., "1y", "6mo").
  - `timeframe` (str): The time interval (e.g., "1m", "5m").
- **Returns:**
  - `float`: The EMA value, or `None` if an error occurs.

### `clean()`
Clears the terminal screen.

- **Returns:**
  - `None`

### `email(server, port, user, password, recipient, subject, body)`
Sends an email with an optional attachment.

- **Parameters:**
  - `server` (str): SMTP server address.
  - `port` (int): SMTP port number.
  - `user` (str): The sender's email address.
  - `password` (str): The sender's email password.
  - `recipient` (str): The recipient's email address.
  - `subject` (str): The email subject.
  - `body` (str): The email body.
- **Returns:**
  - `None`

### `ychart()`
Opens the Yahoo Finance chart page.

- **Returns:**
  - `None`

### `ynews()`
Opens the Yahoo Finance news page.

- **Returns:**
  - `None`

### `change(pair)`
Fetches the exchange rate for the specified currency pair.

- **Parameters:**
  - `pair` (str): The currency pair (e.g., "USDJPY").
- **Returns:**
  - `float`: The exchange rate, or `None` if an error occurs.

### `ath(ticker)`
Fetches the all-time high (ATH) for the specified ticker.

- **Parameters:**
  - `ticker` (str): The ticker symbol of the stock.
- **Returns:**
  - `float`: The all-time high value, or `None` if an error occurs.

### `currency(ticker)`
Fetches the currency in which the specified ticker is traded.

- **Parameters:**
  - `ticker` (str): The ticker symbol of the stock.
- **Returns:**
  - `str`: The currency symbol, or `None` if an error occurs.

### `exchange(ticker)`
Fetches the exchange where the specified ticker is traded.

- **Parameters:**
  - `ticker` (str): The ticker symbol of the stock.
- **Returns:**
  - `str`: The exchange name, or `None` if an error occurs.

### `volume(ticker)`
Fetches the real-time trading volume of the specified ticker.

- **Parameters:**
  - `ticker` (str): The ticker symbol of the stock.
- **Returns:**
  - `int`: The real-time trading volume, or `None` if an error occurs.

### `marketcap(ticker)`
Fetches the market capitalization of the specified ticker.

- **Parameters:**
  - `ticker` (str): The ticker symbol of the stock.
- **Returns:**
  - `int`: The market cap, or `None` if an error occurs.

### `shares(ticker)`
Fetches the number of outstanding shares for the specified ticker.

- **Parameters:**
  - `ticker` (str): The ticker symbol of the stock.
- **Returns:**
  - `int`: The number of shares outstanding, or `None` if an error occurs.

## Usage Examples

Here are a few examples to help you get started:

```python
# Get the bid price of AAPL
print(bid("AAPL"))

# Get the ask price of AAPL
print(ask("AAPL"))

# Start the timer
start_time = start()

# Stop the timer and get elapsed time
elapsed_time = stop(start_time)
print(f"Elapsed Time: {elapsed_time}")

# Log a message
log("Started analysis of AAPL")

# Get the last closing price of AAPL
print(last("AAPL"))

# Calculate the RSI for AAPL
print(rsi("AAPL", 14, "1y", "1h"))

# Calculate the EMA for AAPL
print(ema("AAPL", 200, "1y", "1h"))

# Send an email
email("smtp.gmail.com", 587, "your_email@gmail.com", "password", "recipient_email@gmail.com", "Subject", "Email body")

# Open the Yahoo Finance chart page
ychart()

# Open the Yahoo Finance news page
ynews()

# Get the exchange rate for USD to EUR
print(change("USDEUR"))

# Get the all-time high for AAPL
print(ath("AAPL"))

# Get the currency in which AAPL is traded
print(currency("AAPL"))

# Get the exchange where AAPL is traded
print(exchange("AAPL"))

# Get the real-time trading volume for AAPL
print(volume("AAPL"))

# Get the market cap for AAPL
print(marketcap("AAPL"))

# Get the number of outstanding shares for AAPL
print(shares("AAPL"))
