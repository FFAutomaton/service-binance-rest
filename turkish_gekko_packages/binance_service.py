import time, json, hmac, hashlib, requests, binance, datetime
from datetime import timedelta
from binance.client import Client
import pandas as pd
from urllib.parse import urljoin, urlencode
BASE_URL = 'https://api.binance.com'


class BinanceException(Exception):
    def __init__(self, status_code, data):

        self.status_code = status_code
        if data:
            self.code = data['code']
            self.msg = data['msg']
        else:
            self.code = None
            self.msg = None
        message = f"{status_code} [{self.code}] {self.msg}"

        # Python 2.x
        # super(BinanceException, self).__init__(message)
        super().__init__(message)


class TurkishGekkoBinanceService:
    def __init__(self, config=None):
        self.headers = None
        self.client = None
        self.Config = config
        self.client = self._get_client()
        self.headers = {
            'X-MBX-APIKEY': self.Config.get('API_KEY')
        }

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
    def spot_cuzdan_bakiyesi(self):
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
    def market_satinal(self, symbol, quantity):
        # symbole ornek olarak 'ETHUSDT'
        client = self.client
        try:
            api_resp = client.order_market_buy(symbol=symbol, quantity=quantity)
            # api_resp['status'] = FILLED
            return api_resp
        except:
            None
            return None

    def market_sat(self, symbol, quantity):
        client = self.client
        try:
            api_resp = client.order_market_sell(symbol=symbol, quantity=quantity)
            return api_resp
        except:
            None
            return None

# TODO yuvarlama isi var commentteki satiri aktiflestirmeyi unutma
    @staticmethod
    def order_book(token):
        r = requests.get("https://api.binance.com/api/v3/depth", params=dict(symbol=token))
        results = r.json()
        asks = results['asks']
        bids = results['bids']
        ask_df = pd.DataFrame(asks, columns=['ask_price', 'amount'])
        ask_df.ask_price = ask_df.ask_price.astype('float')
        ask_df.amount = ask_df.amount.astype('float')

        # ask_df.price = ask_df.price.round(0)
        ask_df = ask_df.groupby(['ask_price'])['amount'].sum().reset_index()
        bid_df = pd.DataFrame(bids, columns=['bid_price', 'amount'])
        bid_df.bid_price = bid_df.bid_price.astype('float')
        bid_df.amount = bid_df.amount.astype('float')

        bid_df = bid_df.groupby(['bid_price'])['amount'].sum().reset_index()
        return ask_df, bid_df

    def temp(self):
        # TODO sevki bey burayi daha sonra girilen token valid mi degil mi diye
        # TODO kontrol yapmak icin kullanabiliriz
        # all_symbols = self.client.get_all_isolated_margin_symbols()
        # info = self.client.get_margin_asset(asset='BNB')
        # info = self.client.get_margin_account()
        max_token_miktari = self.client.get_max_margin_transfer(asset='USDT')

        trades = self.client.get_margin_trades(symbol='BNBUSDT')
        all_orders = self.client.get_all_margin_orders(symbol='BNBUSDT')
        acik_orderlar = self.client.get_open_margin_orders()

        # temp = self.client.futures_account_balance()
        anan = self.client.futures_account_balance(asset='USDT', amount=10.0, type=1, timestamp=datetime.datetime.now())
        print(anan[6])

        return 0

    def spottan_margine_transfer(self, token, miktar):
        transaction = self.client.transfer_spot_to_margin(asset=token, amount=miktar)

    def marginden_spota_transfer(self, token, miktar):
        transaction = self.client.transfer_margin_to_spot(asset=token, amount=miktar)

    def futures_hesap_bakiyesi(self):
        return self.client.futures_account_balance()

    def futures_cuzdan_aktarimi(self, token, miktar, nereye):
        """
            nereye`nin cevabi:(int olmasi gerekiyo)
                1 spottan USDT-M futuresa
                2 USDT-M futurestan spota
                3 spottan COIN-M e
                4 COIN-M den spota
        """
        PATH = '/sapi/v1/futures/transfer'
        timstamp = int(time.time() * 1000)
        params = {
            'asset': token,
            'amount': miktar,
            'type': nereye,
            'timestamp': timstamp
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.client.API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, PATH)
        r = requests.post(url, headers=self.headers, params=params)
        if r.status_code == 200:
            data = r.json()
            return json.dumps(data, indent=4)
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())


