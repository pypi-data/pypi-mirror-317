# qwdataapi 

v1.0.7



## Introduction

qwdataapi is a data service API provided by [quantweb.ai](https://quantweb3.ai), used for fetching historical data from various cryptocurrency exchanges and a variety of alternative data.



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

Replace **'Your username'** and **'Your token'** with your actual username and token, which could be obtained from [Quantweb.ai Subscription Page](https://quantweb3.ai/subscribe). After the subscription, these authentication will be sent to your email. It is **free** for the first 7 days. 



## Function Description



### ***fetch_data:***

- #### Function Purpose

The `fetch_data` function is used to retrieve specific asset type and data type information from a designated exchange. The data can include candlestick (k-line) data, among others.



- #### Function Parameters
  - `exchange` (str): The name of the exchange, defaults to `'binance'`.

  - `symbol` (str): The trading pair, for example `'BTCUSDT'`, defaults to `'BTCUSDT'`.

  - `asset_type` (str): The type of asset, defaults to `'spot'`, representing spot trading. `'coinm'` means coin based future trading, `'usdm'` means USD based future trading.

  - `data_type` (str): The type of data, defaults to `'klines'`, representing candlestick data.

  - `start` (str): The start time of the data, formatted as `'YYYY-MM-DD HH:MM:SS'`, defaults to `'2023-08-01 00:00:00'`.

  - `end` (str): The end time of the data, formatted the same as the start time, defaults to `'2024-07-17 00:00:00'`.

  - `batch_size` (int): The size of the data batch for each request, a number between 40 and 100, defaults to `50`.

    


