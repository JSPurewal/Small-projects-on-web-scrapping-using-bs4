import pandas as pd
from pycoingecko import CoinGeckoAPI


def crypto_info(coins,curr): 
    cg = CoinGeckoAPI()
    coins=cryptos
    data=cg.get_price(ids=coins, vs_currencies=curr, include_market_cap=True, include_24hr_vol=True, include_24hr_change=True)
    dtf=pd.DataFrame(data)
    dtf=dtf.transpose()
    return dtf


if __name__ == "__main__":
    cryptos=['ufo-gaming','avalanche-2','binancecoin','joe','bitcoin','olympus','ethereum','cosmos-ecosystem','litecoin', 'monero', 'stellar', 'tether','stablecoins','metaverse']
    currencies=['usd','eur']
    df=crypto_info(cryptos,currencies)
    df.to_csv("Crypto_Today.csv")

    print(df[['usd', 'usd_market_cap', 'usd_24h_vol','eur','eur_market_cap', 'eur_24h_vol']].describe().apply(lambda s: s.apply('{0:,.0f}'.format)))   