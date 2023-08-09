from datetime import date

import pytest

from config import *
from ffautmaton_packages.binance_service import FFAutomatonBinanceService


def test_service():
    config = {'API_KEY': API_KEY, 'API_SECRET': API_SECRET}
    binance_service = FFAutomatonBinanceService(config)
    today = date.today()
    coin = 'ETHUSDT'
    df = binance_service.zaman_serisi_fraktali_olustur(coin, today)
    print(df)
    assert df


def test_api():
    config = {'API_KEY': API_KEY, 'API_SECRET': API_SECRET}
    binance_service = FFAutomatonBinanceService(config)
    yetkiler = binance_service.check_api_permissions()
    if yetkiler is not None:
        pytest.fail(yetkiler)
    else:
        pass


def test_cuzdan():
    config = {'API_KEY': API_KEY, 'API_SECRET': API_SECRET}
    binance_service = FFAutomatonBinanceService(config)
    futures_cuzdan = binance_service.futures_hesap_bakiyesi()
    temp = list(futures_cuzdan.values())
    bakiye = 0
    for i in temp:
        bakiye = bakiye + float(i)
    if bakiye == 0:
        pytest.fail(bakiye)
    return bakiye

if __name__ == "__main__":
    print(test_cuzdan())
