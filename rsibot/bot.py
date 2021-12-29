import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
RSI_PRIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.005

closes = []
in_position = False

# change the country here 
client = Client(config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY, tld='us')  
# ORDER FUNCTION
def order(side, quantiy, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("Sending Order")
        order = client.create_order(symbol=symbol, 
        side=side,
        type=order_type,
        quantity=quantity)
        print(order)
    except Exeption as e:
        return False
    return True
   
def on_open(ws):
    print('Opened Connection')
    
def on_close(ws):
    print('Closed Connection')
    
def on_message(ws, message):
    global closes
    
    print('Received Message')
    json_message = json.loads(message)
    pprint.pprint(json_message)
     
    candle = json_message['k']
    
    is_candle_closed = candle['x']
    close = candle['c']
    
    if is_candle_closed:
        print("Candle Closed at {}".format(close))
        close.append(float(close))
        print("Closes")
        print(closes)
        
        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("All RSIs Calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("The Current  RSI is {}".format(last_rsi))
            
            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("OVERBOUGHT! Sell! Sell! Sell!!!")
                    # Binance SELL-ORDER Logic here 
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL):
                    if order_succeeded:
                        in_position = False
                else: 
                    print("It is OVER BOUGHT, but We don't own any. Nothing to do.")
            
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("It is OVERSOLD, but you already own it. Nothing to do")
                else:
                    print("OVERSOLD! Buy! Buy! Buy!!!")
                    # Binance BUY-ORDER Logic here 
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL):
                    if order_succeeded:
                        in_position = True
            
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
