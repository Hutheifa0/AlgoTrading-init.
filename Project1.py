from Api import PublicKey, SecretKey, token, chat
from binance import Client
import pandas as pd
import time
import requests


client = Client(PublicKey, SecretKey)

def SendTelegramMessage(message):
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat, "text": message})



while True:
    try:
        _Symbol = "BTCUSDT"
        Time_Frame = Client.KLINE_INTERVAL_1MINUTE
        Period = "2 day ago UTC"

        klines = client.get_historical_klines(_Symbol, Time_Frame, Period)
        df = pd.DataFrame(klines)
        df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', '6', '7', '8', '9', '10', '11']
        del df['6'], df['7'], df['8'], df['9'], df['10'], df['11']

        # convert numeric columns
        df['Open'] = pd.to_numeric(df['Open'])
        df['High'] = pd.to_numeric(df['High'])
        df['Close'] = pd.to_numeric(df['Close'])
        df['Low'] = pd.to_numeric(df['Low'])
        df['Volume'] = pd.to_numeric(df['Volume'])

        df['Time'] = pd.to_datetime(df['Time'], unit='ms')

        # EMA Strategy
        candle1 = 10
        df[f"EMA_{candle1}"] = df['Close'].ewm(span=candle1, adjust=False).mean()

        Open_Last = df['Open'].iloc[-1]
        Open_SecondLast = df['Open'].iloc[-2]

        Open_Last_EMA = df[f'EMA_{candle1}'].iloc[-1]
        Open_SecondLast_EMA = df[f'EMA_{candle1}'].iloc[-2]

        print(df.tail(3))
    
        # Buy
        # Buy signal example:
        if (Open_SecondLast < Open_SecondLast_EMA and Open_Last > Open_Last_EMA ):
            SendTelegramMessage("Bullish Signal with RSI confirmation")
        
        # Sell signal example:
        if (Open_SecondLast > Open_SecondLast_EMA and Open_Last < Open_Last_EMA) :
            SendTelegramMessage("Bearish Signal with RSI confirmation")
        
    except Exception as e:
        print(f"Error in loop: {e}")

    time.sleep(1)



