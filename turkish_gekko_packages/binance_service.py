from datetime import timedelta

import binance
from binance.client import Client


class TurkishGekkoBinanceService:
    def __init__(self, config=None):
        self.client = None
        self.Config = config
        self.client = self._get_client()

    def _get_client(self):
        return Client(self.Config.get('API_KEY'), self.Config.get('API_SECRET'))

    def get_client(self):
        if not self.client:
            self.client = self._get_client()
        return self.client

    def zaman_serisi_fraktali_olustur(self, coin, today, WINDOW_DAY=1, WINDOW_4H=7*6,
                                      WINDOW_1H=4*24, WINDOW_15M=2*24*4):

        client = self.get_client()
        today = today - timedelta(days=1)
        lastsevenday = str(today - timedelta(days=7))
        lastfourday = str(today - timedelta(days=4))
        lasttwoday = str(today - timedelta(days=2))
        today = str(today)

        dayklines = client.get_historical_klines(
            symbol=coin, interval=client.KLINE_INTERVAL_1DAY,
            start_str=today, end_str=today, limit=WINDOW_DAY
        )
        fourhourklines = client.get_historical_klines(
            symbol=coin, interval=client.KLINE_INTERVAL_4HOUR,
            start_str=lastsevenday, end_str=today, limit=WINDOW_4H
        )
        hourlyklines = client.get_historical_klines(
            symbol=coin, interval=client.KLINE_INTERVAL_1HOUR,
            start_str=lastfourday, end_str=today, limit=WINDOW_1H
        )
        fifteenminklines = client.get_historical_klines(
            symbol=coin, interval=client.KLINE_INTERVAL_15MINUTE,
            start_str=lasttwoday, end_str=today, limit=WINDOW_15M
        )

        return dayklines, fourhourklines, hourlyklines, fifteenminklines

    def check_api_permissions(self):
        client = self.client
        _temp = client.get_account_api_permissions()
        if _temp['ipRestrict'] is True:
            return 'Has ip restriction'
        elif _temp['enableSpotAndMarginTrading'] is False:
            return 'Has no Spot and Margin trade permission'
        else:
            return None

# Bunu sonradan nerde ne asset var bilmedigim bi hesaba baglarsam her seyi
# satip sonra all in all out stratejisine gecebilmek icin yazdim
    def balance_founder(self):
        not_zero_balances = []
        quantities = []
        _temp = self.get_client().get_account()
        balances = _temp['balances']
        for i in balances:
            condition = float(i['free'])
            if condition != 0.0:
                not_zero_balances.append(i['asset'])
                quantities.append(i['free'])
        if len(not_zero_balances) == 0:
            return None
        resp = dict(zip(not_zero_balances, quantities))

        return resp

# TODO bu market buyla selle BinanceOrderMinAmountException gibi exceptionlari ekleyelim
# TODO baya kaya kadar saglam olur o sekilde das gibi olur dasss
    def market_buy(self, symbol, quantity):
        # symbole ornek olarak 'ETHUSDT'
        client = self.client
        try:
            api_resp = client.order_market_buy(symbol=symbol, quantity=quantity)
            # api_resp['status'] = FILLED
            return api_resp
        except:
            None
            return None

    def market_sell(self, symbol, quantity):
        client = self.client
        try:
            api_resp = client.order_market_sell(symbol=symbol, quantity=quantity)
            return api_resp
        except:
            None
            return None
