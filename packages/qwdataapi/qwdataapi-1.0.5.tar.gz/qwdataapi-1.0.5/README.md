# qwdataapi 

v1.0.5



## Introduction

qwdataapi is a data service API provided by [quantweb.ai](https://www.quantweb3.ai), used for fetching historical data from various cryptocurrency exchanges and a variety of alternative data.



## Installation Instructions

Installation can be done using pip:

```bash
pip install qwdataapi
```



## Usage Instructions

Three steps to obtain minute-level market data:

```python
from qwdataapi import *

auth('Your username', 'Your token')
df = fetch_data(symbol='BTCUSDT', start='2023-07-01 00:00:00')
print(df.head())
```

Replace **'Your username'** and **'Your token'** with your actual username and token, which could be obtained from [quantweb.ai](https://www.quantweb3.ai), 



## Function Description



### ***fetch_data:***

- #### Function Purpose

The `fetch_data` function is used to retrieve specific asset type and data type information from a designated exchange. The data can include candlestick (k-line) data, among others.



- #### Function Parameters
  - `exchange` (str): The name of the exchange, defaults to `'binance'`.

  - `symbol` (str): The trading pair, for example `'BTCUSDT'`, defaults to `'BTCUSDT'`.

  - `asset_type` (str): The type of asset, defaults to `'spot'`, representing spot trading.

  - `data_type` (str): The type of data, defaults to `'klines'`, representing candlestick data.

  - `start` (str): The start time of the data, formatted as `'YYYY-MM-DD HH:MM:SS'`, defaults to `'2023-08-01 00:00:00'`.

  - `end` (str): The end time of the data, formatted the same as the start time, defaults to `'2024-07-17 00:00:00'`.

  - `batch_size` (int): The size of the data batch for each request, a number between 40 and 100, defaults to `50`.

    

- #### Usage Example

```python
# Import the fetch_data function
from client import fetch_data

# Call the function to retrieve data
df = fetch_data(exchange='binance', symbol='ETHUSDT', start='2023-09-01 00:00:00', end='2023-09-30 23:59:59')

# View the retrieved data
print(df.head())
```

```
