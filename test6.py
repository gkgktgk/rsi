import pyupbit
import requests
import time
import pandas as pd
import jwt
import uuid
from urllib.parse import urlencode
import datetime

access = "xb8xGYjZktxXq3w2hLMD12YuKorydko09Np5rxyf"
secret = "fuuWvsOck4w9VSixTB12C88Xyc92Q9GIIug8KyOU"
upbit = pyupbit.Upbit(access, secret)

payload = {
    'access_key': access,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}
res = requests.get("https://api.upbit.com" + "/v1/accounts", headers=headers)



def get_ma(df, n):
    return df['close'].rolling(window=n).mean()

def rsi_upbit(itv, symbol):
    url = "https://api.upbit.com/v1/candles/minutes/"+str(itv)
    querystring = {"market" : symbol, "count" : "200"}
    response = requests.request("GET", url, params=querystring)
    data = response.json()
    df =pd.DataFrame(data)
    df=df.reindex(index=df.index[::-1]).reset_index()
    nrsi=rsi_calc(df, 14).iloc[-1]
    print("현재" + str(itv) +"분"  + str(symbol) + "rsi :" +str(nrsi))

    return nrsi


def rsi_calc(ohlc: pd.DataFrame, period: int = 14):
    ohlc["trad_price"] = ohlc["trade_price"]
    delta = ohlc["trade_price"].diff()
    gains, declines = delta.copy(), delta.copy()
    gains[gains < 0] = 0
    declines[declines > 0] = 0

    _gain = gains.ewm(com=(period-1), min_periods=period).mean()
    _loss = declines.abs().ewm(com=(period-1), min_periods=period).mean()

    RS = _gain / _loss
    return pd.Series(100-(100/(1+RS)), name="RSI")      



#시장가 매수 - 만원
def buy_10000(symbol) :
    upbit.buy_market_order(symbol, 10000)

# 시장가 매도 
def sell(symbol, balance) :
    upbit.sell_market_order(symbol, balance)

# 미체결 주문 조회
def get_order(symbol):
    upbit.get_order(symbol)

def sell_2percent(tickle):
    sell_flag = 0
    balance = upbit.get_balance("KRW-"+tickle)

    for item in account :   
        if item["currency"] == tickle :
                avg_price = float(item["avg_buy_price"])
                percent = (pyupbit.get_current_price("KRW-"+tickle) / avg_price -1) * 100
                print(tickle, avg_price, percent)
    
    # time.sleep(0.1)
    if percent > 2 :
        sell("KRW-"+tickle, balance)
        sell_flag=1
    elif percent < -2 :
        sell("KRW-"+tickle, balance)
        sell_flag=1
    return sell_flag


flag_BTC = 0
flag_ETH = 0
flag_JST = 0
flag_SAND = 0
flag_BORA = 0
flag_LSK = 0
flag_XRP = 0
flag_WEMIX = 0
flag_MANA = 0
flag_FLOW = 0
flag_WAVES = 0
flag_NU = 0
flag_AXS = 0

buy_BTC = 0
buy_ETH = 0
buy_JST = 0
buy_SAND = 0
buy_BORA = 0
buy_LSK = 0
buy_XRP = 0
buy_WEMIX = 0
buy_MANA = 0
buy_FLOW = 0
buy_WAVES = 0
buy_NU = 0
buy_AXS = 0

# list_coin = ["KRW-ETH" "KRW-BTC" "KRW-JST" "KRW-SAND" "KRW-BORA" "KRW-LSK" "KRW-XRP"]

while True:
    df_ETH = pyupbit.get_ohlcv("KRW-ETH", interval="minute1", count=30)
    df_BTC = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=30)
    df_JST = pyupbit.get_ohlcv("KRW-JST", interval="minute1", count=30)
    df_SAND = pyupbit.get_ohlcv("KRW-SAND", interval="minute1", count=30)
    df_BORA = pyupbit.get_ohlcv("KRW-BORA", interval="minute1", count=30)
    df_LSK = pyupbit.get_ohlcv("KRW-LSK", interval="minute1", count=30)
    df_XRP = pyupbit.get_ohlcv("KRW-XRP", interval="minute1", count=30)
    df_WEMIX = pyupbit.get_ohlcv("KRW-WEMIX", interval="minute1", count=30)
    df_MANA = pyupbit.get_ohlcv("KRW-MANA", interval="minute1", count=30)
    df_FLOW = pyupbit.get_ohlcv("KRW-FLOW", interval="minute1", count=30)
    df_WAVES = pyupbit.get_ohlcv("KRW-WAVES", interval="minute1", count=30)
    df_NU = pyupbit.get_ohlcv("KRW-NU", interval="minute1", count=30)
    df_AXS = pyupbit.get_ohlcv("KRW-AXS", interval="minute1", count=30)

    balance_ETH = upbit.get_balance("KRW-ETH")
    balance_BTC = upbit.get_balance("KRW-BTC")
    balance_JST = upbit.get_balance("KRW-JST")
    balance_SAND = upbit.get_balance("KRW-SAND")
    balance_BORA = upbit.get_balance("KRW-BORA")
    balance_LSK = upbit.get_balance("KRW-LSK")
    balance_XRP = upbit.get_balance("KRW-XRP")
    balance_WEMIX = upbit.get_balance("KRW-WEMIX")
    balance_MANA = upbit.get_balance("KRW-MANA")
    balance_FLOW = upbit.get_balance("KRW-FLOW")
    balance_WAVES = upbit.get_balance("KRW-WAVES")
    balance_NU = upbit.get_balance("KRW-NU")
    balance_AXS = upbit.get_balance("KRW-AXS")

    account = res.json()

    

#BTC
    if balance_BTC == 0 and buy_BTC < 1:                        # 갖고 있는 코인 없음
        rsi_now_BTC = rsi_upbit(30, symbol="KRW-BTC")
        time.sleep(0.1)

        if rsi_now_BTC <= 28 :
            flag_BTC = 1
        
        if rsi_now_BTC >= 33 and flag_BTC > 0 :
            buy_10000("KRW-BTC")
            flag_BTC = 0
            buy_BTC = 1
            
    elif balance_BTC != 0 :                      # 잔고 코인 존재
        # 매도 체크 
        # rsi_now_BTC = rsi_upbit(30, symbol="KRW-BTC")
        if sell_2percent(tickle = "BTC") == 1 :
            buy_BTC = 0    

#ETH
    if balance_ETH == 0 and buy_ETH < 1:                        # 갖고 있는 코인 없음
        rsi_now_ETH = rsi_upbit(30, symbol="KRW-ETH")
        time.sleep(0.1)

        if rsi_now_ETH <= 28 :
            flag_ETH = 1
        
        if rsi_now_ETH >= 33 and flag_ETH > 0 :
            buy_10000("KRW-ETH")
            flag_ETH = 0
            buy_ETH = 1
            
    elif balance_ETH != 0 :                      # 잔고 코인 존재
        # 매도 체크 
        if sell_2percent(tickle = "ETH") == 1 :
            buy_ETH = 0 

#JST
    if balance_JST == 0 and buy_JST < 1:                        # 갖고 있는 코인 없음
        rsi_now_JST = rsi_upbit(30, symbol="KRW-JST")
        time.sleep(0.1)

        if rsi_now_JST <= 28 :
            flag_JST = 1
        
        if rsi_now_JST >= 33 and flag_JST > 0 :
            buy_10000("KRW-JST")
            flag_JST = 0
            buy_JST = 1

            
    elif balance_JST != 0 :                      # 잔고 코인 존재
        # 매도 체크 
        if sell_2percent(tickle = "JST") == 1 :
            buy_JST = 0 


#SAND
    if balance_SAND == 0 and buy_SAND < 1:                        # 갖고 있는 코인 없음
        rsi_now_SAND = rsi_upbit(30, symbol="KRW-SAND")
        time.sleep(0.1)

        if rsi_now_SAND <= 28 :
            flag_SAND = 1
        
        if rsi_now_SAND >= 33 and flag_SAND > 0 :
            buy_10000("KRW-SAND")
            flag_SAND = 0
            buy_SAND = 1

            
    elif balance_SAND != 0 :                      # 잔고 코인 존재
        # 매도 체크 
        if sell_2percent(tickle = "SAND") == 1 :
            buy_SAND = 0  
#BORA
    if balance_BORA == 0 and buy_BORA < 1:                        # 갖고 있는 코인 없음
        rsi_now_BORA = rsi_upbit(30, symbol="KRW-BORA")
        time.sleep(0.1)

        if rsi_now_BORA <= 28 :
            flag_BORA = 1
        
        if rsi_now_BORA >= 33 and flag_BORA > 0 :
            buy_10000("KRW-BORA")
            flag_BORA = 0
            buy_BORA = 1

            
    elif balance_BORA != 0 :                      # 잔고 코인 존재
        # 매도 체크 
        if sell_2percent(tickle = "BORA") == 1 :
            buy_BORA = 0 

#LSK                 
    if balance_LSK == 0 and buy_LSK < 1:                        # 갖고 있는 코인 없음
        rsi_now_LSK = rsi_upbit(30, symbol="KRW-LSK")
        time.sleep(0.1)

        if rsi_now_LSK <= 28 :
            flag_LSK = 1
        
        if rsi_now_LSK >= 33 and flag_LSK > 0 :
            buy_10000("KRW-LSK")
            flag_LSK = 0
            buy_LSK = 1

            
    elif balance_LSK != 0 :                      # 잔고 코인 존재
        # 매도 체크 
        if sell_2percent(tickle = "LSK") == 1 :
            buy_LSK = 0 

#XRP
    if balance_XRP == 0 and buy_XRP < 1:                        # 갖고 있는 코인 없음
        rsi_now_XRP = rsi_upbit(30, symbol="KRW-XRP")
        time.sleep(0.1)

        if rsi_now_XRP <= 28 :
            flag_XRP = 1
        
        if rsi_now_XRP >= 33 and flag_XRP > 0 :
            buy_10000("KRW-XRP")
            flag_XRP = 0
            buy_XRP = 1

            
    elif balance_XRP != 0 :                      # 잔고 코인 존재
        # 매도 체크 
        if sell_2percent(tickle = "XRP") == 1 :
            buy_XRP = 0 

#WEMIX
    if balance_WEMIX == 0 and buy_WEMIX < 1:                        # 갖고 있는 코인 없음
        rsi_now_WEMIX = rsi_upbit(30, symbol="KRW-WEMIX")
        time.sleep(0.1)

        if rsi_now_WEMIX <= 28 :
            flag_WEMIX = 1
        
        if rsi_now_WEMIX >= 33 and flag_WEMIX > 0 :
            buy_10000("KRW-WEMIX")
            flag_WEMIX = 0
            buy_WEMIX = 1

            
    elif balance_WEMIX != 0 :                      # 잔고 코인 존재
        # 매도 체크 
        if sell_2percent(tickle = "WEMIX") == 1 :
            buy_WEMIX = 0 

#MANA
    if balance_MANA == 0 and buy_MANA < 1:                        # 갖고 있는 코인 없음
        rsi_now_MANA = rsi_upbit(30, symbol="KRW-MANA")
        time.sleep(0.1)

        if rsi_now_MANA <= 28 :
            flag_MANA = 1
        
        if rsi_now_MANA >= 33 and flag_MANA > 0 :
            buy_10000("KRW-MANA")
            flag_MANA = 0
            buy_MANA = 1

            
    elif balance_MANA != 0 :                      # 잔고 코인 존재
        # 매도 체크 
        if sell_2percent(tickle = "MANA") == 1 :
            buy_MANA = 0 

#FLOW
    if balance_FLOW == 0 and buy_FLOW < 1:                        # 갖고 있는 코인 없음
        rsi_now_FLOW = rsi_upbit(30, symbol="KRW-FLOW")
        time.sleep(0.1)

        if rsi_now_FLOW <= 28 :
            flag_FLOW = 1
        
        if rsi_now_FLOW >= 33 and flag_FLOW > 0 :
            buy_10000("KRW-FLOW")
            flag_FLOW = 0
            buy_FLOW = 1

            
    elif balance_FLOW != 0 :                      # 잔고 코인 존재
        # 매도 체크 
        if sell_2percent(tickle = "FLOW") == 1 :
            buy_FLOW = 0     

#WAVES
    if balance_WAVES == 0 and buy_WAVES < 1:                        # 갖고 있는 코인 없음
        rsi_now_WAVES = rsi_upbit(30, symbol="KRW-WAVES")
        time.sleep(0.1)

        if rsi_now_WAVES <= 28 :
            flag_WAVES = 1
        
        if rsi_now_WAVES >= 33 and flag_WAVES > 0 :
            buy_10000("KRW-WAVES")
            flag_WAVES = 0
            buy_WAVES = 1

            
    elif balance_WAVES != 0 :                      # 잔고 코인 존재
        # 매도 체크 
        if sell_2percent(tickle = "WAVES") == 1 :
            buy_WAVES = 0      

#NU
    if balance_NU == 0 and buy_NU < 1:                        # 갖고 있는 코인 없음
        rsi_now_NU = rsi_upbit(30, symbol="KRW-NU")
        time.sleep(0.1)

        if rsi_now_NU <= 28 :
            flag_NU = 1
        
        if rsi_now_NU >= 33 and flag_NU > 0 :
            buy_10000("KRW-NU")
            flag_NU = 0
            buy_NU = 1

            
    elif balance_NU != 0 :                      # 잔고 코인 존재
        # 매도 체크 
        if sell_2percent(tickle = "NU") == 1 :
            buy_NU = 0    

#AXS
    if balance_AXS == 0 and buy_AXS < 1:                        # 갖고 있는 코인 없음
        rsi_now_AXS = rsi_upbit(30, symbol="KRW-AXS")
        time.sleep(0.1)

        if rsi_now_AXS <= 28 :
            flag_AXS = 1
        
        if rsi_now_AXS >= 33 and flag_AXS > 0 :
            buy_10000("KRW-AXS")
            flag_AXS = 0
            buy_AXS = 1

            
    elif balance_AXS != 0 :                      # 잔고 코인 존재
        # 매도 체크 
        if sell_2percent(tickle = "AXS") == 1 :
            buy_AXS = 0    

    print(datetime.datetime.now())        
    print("---------------------------------------------------------------")    
