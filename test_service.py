from datetime import date

import pytest

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


def test_api():
    config = {'API_KEY': API_KEY, 'API_SECRET': API_SECRET}
    binance_service = TurkishGekkoBinanceService(config)
    yetkiler = binance_service.check_api_permissions()
    if yetkiler is not None:
        pytest.fail(yetkiler)
    else:
        pass


def test_cuzdan():
    config = {'API_KEY': API_KEY, 'API_SECRET': API_SECRET}
    binance_service = TurkishGekkoBinanceService(config)
    spot_cuzdan = binance_service.spot_cuzdan_bakiyesi()
    temp = list(spot_cuzdan.values())
    bakiye = 0
    for i in temp:
        bakiye = bakiye + float(i)
    if bakiye == 0:
        pytest.fail(bakiye)


