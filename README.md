# service-binance-rest

Bu repo binance rest API'ina baglanmak icin FFAutomaton organizasyonu kafasindadir.

Her turlu destege acigiz.


# Fonksiyonlar

+ check_api_permissions()        
+ zaman_serisi_fraktali_olustur()
+ spot_cuzdan_bakiyesi()
+ market_satinal()/market_sat()
+ order_book()
+ spottan_margine_transfer()
+ marginden_spota_transfer()
+ futures_hesap_bakiyesi()
+ futures_cuzdan_aktarimi()
+ hesap_trade_gecmisi()
+ futures_market_islem()
+ futures_islem_gecmisi()
+ futures_market_exit()


## Testing
Yazdigimiz her kod icin test yazmamiz lazim, ornek bir testi repoda bulabilirsiniz. Pytest ve unittest kutuphanelerini
kullanabiliriz.
Servisi test etmek icin config.py olusturmali ve icine `API_KEY` = "xxxx" `API_SECRET` = "xxxxxx" degiskenlerini
koymalisiniz.



