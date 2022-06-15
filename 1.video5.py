from pprint import pprint
from binance.spot import Spot
import config5
import pandas as pd
class RobotBinance:
    """
    Bot para Binance que permite automatizar las compras y ventas en el mercado spot
    """
    __api_key = config5.API_KEY
    __api_secret = config5.API_SECRET_KEY
    binance_client= Spot(key=__api_key, secret=__api_secret) # inicia la conexion con binance en el mercado spot

    def __init__(self,pair:str,temporality:str):
        self.pair1=pair.upper()
        self.temporality=temporality
        self.symbol= self.pair1.removesuffix("USDT")

    def _request(self,endpoint:str, parameters: dict = None):
        #while True:
            try:
                response = getattr(self.binance_client,endpoint) # => self.binance_client.endpoint
                return response(recvWindow=60000) if parameters is None else response(**parameters)
            except:
                print("aja9")

    def binance_account(self,RW:int=None,TS:int=None) -> dict:
        """
        Devuelve las metricas y balances asociados a la cuenta.
        :rtype: object
        :return:cuenta de binance
        """
        numberRW = 59000 if RW is None else RW
        numberTS = 50 if TS is None else TS
        return self._request("account")            # se visualizan 512 asset(activos)

    def cryptocurrencies(self) -> dict:
        """
        Devuelve una lista con todas las criptomonedas en la cuenta que tengan un saldo positivo
        return:Criptomonedas
        """
        return [crypto for crypto in self.binance_account().get("balances") if float(crypto.get("free")) > 0]

    def symbol_price(self, pair: str = None):
        """
        Devuelve el precio para un determinado par
        :param pair: criptomoneda a determinar el precio ["BTCUSDT","  ETHUSDT   "]
        :return:precio del par
        """
        symbol = self.pair1 if pair is None else pair
        return float(self._request("ticker_price",{"symbol":symbol.upper()}).get("price"))

    def candlestick(self,limit:int=50) ->pd.DataFrame:
        """
        Devuelve la informacion de las velas.
        :return:velas japonesas
        """
        candle = pd.DataFrame(self.binance_client.klines(
            symbol=self.pair1,
            interval=self.temporality,
            limit=limit
        ),
            columns=["Open Time","Open","High","Low","Close","Volume","Close Time","quote asset volume","number of trade","Taker buy base asset volume","taker buy quote asset volume","ignore"
            ],
            dtype=float
        )
        return candle[["Open Time","Close Time","Open","High","Low","Close","Volume"]]



bot=RobotBinance("ethusdt","8h")

#print(type(bot.binance_client))
        #<class 'binance.spot.Spot'>

#print(type(bot.symbol_price))
        #<class 'method'>

#pprint(dir(bot.binance_client))
        # devuelve todos los metodos del objeto Binance_client

#print(bot.candlestick())

#print(bot.binance_client) 
        #devuelve <binance.spot.Spot object at 0x0000005BC146C520>

#print(type(bot.binance_client())) no se ejecuta porque no es metodo de clase si no atributo

#pprint(bot.binance_client().klines("BTCUSDT","4h"))

#pprint(bot.binance_client.account(recvWindow=60000))

#pprint(getattr(bot.binance_client,"account")) 
        #da la localizacion del la respuesta en la memoria
        #<bound method account of <binance.spot.Spot object at 0x000000BC4B2FC520>>

#pprint(getattr(bot.binance_client,"account")(recvWindow=60000))
        #aca devuelve los datos (balances) porque se hiso la llamada

#print(bot.symbol_price())
#print("hola mundo cruel, what's up denger¡")

#pprint(bot.binance_account)
        #<bound method RobotBinance.binance_account of <__main__.RobotBinance object at 0x0000005E6F2538B0>>
#pprint(type(bot.binance_account))
        #<class 'method'>

#pprint(bot.symbol_price())

#pprint(dir(Spot))

pprint(bot.binance_account())
