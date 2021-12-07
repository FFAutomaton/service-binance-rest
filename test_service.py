from datetime import date
from config import *
from turkish_gekko_packages.binance_service import TurkishGekkoBinanceService


def test_service():
    config = {'API_KEY': API_KEY, 'API_SECRET': API_SECRET}
    binance_service = TurkishGekkoBinanceService(config)
    today = date.today()
    coin = 'ETHUSDT'
    df = binance_service.zaman_serisi_fraktali_olustur(coin, today)
    print(df)
    assert df
