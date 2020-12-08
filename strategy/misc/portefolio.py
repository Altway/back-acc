import pypfopt
from pypfopt import (
    EfficientFrontier, HRPOpt,  objective_functions, 
    CLA, risk_models, expected_returns, plotting
)
### Import
from pycoingecko import CoinGeckoAPI
from datetime import datetime
from pprint import pprint
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

def ici():

    client = CoinGeckoAPI()

    ### Configuration
    from_date_str = "01-01-2019"
    to_date_str = "01-11-2020"

    from_date = datetime.strptime(from_date_str, '%d-%m-%Y')
    to_date = datetime.strptime(to_date_str, '%d-%m-%Y')
    # SNX Missing

    coins_list = [
        'bitcoin', 'ethereum', 'tezos', 'binancecoin', 
        'litecoin', 'chainlink', 'polkadot', 'eos', 'stellar', 
        'aave', 'uniswap', 'maker', 'yearn-finance', 'compound-governance-token', 'algorand', 
        'icon', 'ampleforth', 'kyber-network', 'enjincoin', 'elrond-erd-2', 'solana','balancer', 'cosmos', 
        'ftx-token', '0x', 'algorand'
    ]

    coins_list = [
        'bitcoin', 'ethereum', 'binancecoin', 
        'litecoin', 'chainlink', 'eos', 'stellar', 
        'aave', 'uniswap', 'maker', 'yearn-finance', 'compound-governance-token', 'algorand', 
        'kyber-network', 'ftx-token', '0x',# 'algorand'
    ]

    coins_list = [
        'bitcoin', 'ethereum', 'binancecoin', 
        'chainlink', 'eos',
    ]
    a = client.get_coin_by_id('ethereum')
    CONFIG_DICT = {
        "risk_free_rate_of_return" : 2,
        "risk_condition": 2,
        "completness_condition": 100,
    }

    ### Historical Data
    to_csv = {}
    list_csv = []
    tickers = {}
    for coin in coins_list:
        _ = client.get_coin_market_chart_range_by_id(coin, 'usd', datetime.timestamp(from_date), datetime.timestamp(to_date))

        prices_list = _['prices']
        total_volumes_list = _['total_volumes']
        market_caps_list = _['market_caps']
        
        flat_timestamp = [el[0] for el in prices_list]
        flat_price = [el[1] for el in prices_list]
        flat_total_volume = [el[1] for el in total_volumes_list]
        flat_market_cap = [el[1] for el in market_caps_list]

        tmp = []

        for i in range(len(flat_timestamp)):
            _ = {}
            #_["timestamp"] = datetime.utcfromtimestamp(int(flat_timestamp[i]/1000)).strftime('%Y-%m-%d %H:%M:%S')
            #_["price"] = flat_price[i]
            #_["total_volume"] = flat_total_volume[i]
            #_["market_cap"] = flat_market_cap[i]
            
            #_[datetime.utcfromtimestamp(int(flat_timestamp[i]/1000)).strftime('%Y-%m-%d %H:%M:%S')] = {"price": flat_price[i], "total_volume": flat_total_volume[i], "market_cap": flat_market_cap[i]}
            tmp.append({
                #"date": datetime.utcfromtimestamp(int(flat_timestamp[i]/1000)).strftime('%Y-%m-%d %H:%M:%S'),
                "date": pd.Timestamp(flat_timestamp[i], unit='ms', tz="UTC"),
                "price": flat_price[i], 
                "total_volume": flat_total_volume[i], 
                "market_cap": flat_market_cap[i],
                "coin_name": coin,
            })
        df = pd.DataFrame(tmp, columns=("date", "price", "total_volume","market_cap", "coin_name"))
        # test = pd.MultiIndex.from_tuples(to_csv, names=["first", "second", "third", "fourth", "fifth"])
        #df = pd.DataFrame(list_csv, columns=("timestamp", "price", "total_volume","market_cap", "coin_name")) 
        df.set_index(["date"])
        tickers[coin] = df
        #pprint(tmp)
        #to_csv.append(tmp)
        #list_csv.append(tmp)
        #to_csv.update(tmp)

    pprint(tickers["bitcoin"])
    #pprint(list_csv)
    #test = [timestamp, prices_list, total_volumes_list, market_caps_list]
    #test = zip(timestamp, prices_list[1], total_volumes_list[1], market_caps_list[1])
    #test = zip(timestamp, a, b, c)
    #csv_dict = {"timestamp": timestamp, "prices": prices_list, "total_volumes": total_volumes_list, "market_caps": market_caps_list}



    ### Calcul des Perfs/Volatilité Weekly/Daily

    for coin in coins_list:
        _ = tickers[coin]
        _["daily_perfs"] = _["price"].pct_change()
        _["cum_daily_perfs"] = _["daily_perfs"].cumsum()
        #print(_.loc[(_["date"].dt.day_name() == 'Monday')]['price'].pct_change())
        _["weekly_perfs"] = _.loc[(_["date"].dt.day_name() == 'Monday')]['price'].pct_change()
        _["cum_weekly_perfs"] = _["weekly_perfs"].cumsum()
        #_["weekly_perfs"] = _.lo
        #print(_)
        #print(_["weekly_perfs"])
        #_["weekly_perfs"] = _["price"].pct_change(freq='M')

    pd.set_option("display.max_rows", 10, "display.max_columns", 30)
    print(tickers["bitcoin"])

    print(tickers["bitcoin"].info())
    tickers["bitcoin"].describe()


    ### Covariance
    import pypfopt
    from pypfopt import (
        EfficientFrontier, HRPOpt,  objective_functions, 
        CLA, risk_models, expected_returns, plotting
    )


    from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

    #Test avec les différent join pour les ticker soù les dimensions de prix ne matchent pas
    # min_periods dans la covar pour enlever si il n'y a pas assez de data
    price_matrix = pd.concat([tickers[coin]["price"].rename(coin) for coin in coins_list], axis=1, join='inner')
    #price_matrix.cov()
    #price_matrix.reset_index(drop=True, inplace=True)
    # pour rajouter les date au dataframe de prix
    #date_price_matrix = pd.concat([tickers[coin]["date"], price_matrix], axis=1, join='inner')
    #df = date_price_matrix
    df = price_matrix
    print(price_matrix)




    ### NORMAL EMA/MEAN HISTORICAL VALUE

    #mu = expected_returns.mean_historical_return(df)
    #mu = expected_returns.ema_historical_return(df)
    mu = expected_returns.capm_return(df)
    #mu = expected_returns.returns_from_prices(df)
    #mu = expected_returns.prices_from_returns(df)

    #S = risk_models.sample_cov(df)
    #S = risk_models.semicovariance(df)
    #S = risk_models.exp_cov(df)
    #S = risk_models.min_cov_determinant(df)
    #S = risk_models.CovarianceShrinkage(df.cov(min_periods=15))
    #S = risk_models.risk_matrix(prices=df, method='ledoit_wolf')
    #S = risk_models.risk_matrix(prices=df, method='ledoit_wolf_single_factor')
    S = risk_models.risk_matrix(prices=df, method='oracle_approximating')

    #mu.plot.barh(figsize=(10,5))
    #plotting.plot_covariance(S, plot_correlation=True)



    # Pretend that you started with a default-weight allocation
    initial_weights = np.array([1/len(tickers)] * len(tickers))

    ef = EfficientFrontier(mu, S, weight_bounds=(-1, 1), gamma=1)
    ef.add_objective(objective_functions.transaction_cost, w_prev=initial_weights, k=0.001) # 1% broker commission
    ef.add_objective(objective_functions.L2_reg, gamma=0.05)  # default is gamma=1

    #ef.min_volatility()
    #ef.max_sharpe()
    ef.max_quadratic_utility()
    #ef.min_efficient_risk(0.5)
    #ef.min_efficient_return(0.5)


    cleaned_weights = ef.clean_weights()
    print(cleaned_weights)
    ef.portfolio_performance(verbose=True, risk_free_rate=0.02)

    pd.Series([abs(i) for i in cleaned_weights.values()]).plot.pie(figsize=(10,10))

    latest_prices = get_latest_prices(df)
    da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value=35802, short_ratio=0.3)

    allocation, leftover = da.lp_portfolio()
    #allocation, leftover = da.greedy_portfolio()

    print("Discrete allocation:", allocation)
    print("Funds remaining: ${:.2f}".format(leftover))

    #pd.Series(cleaned_weights).plot.pie(figsize=(10,10))
    return allocation, cleaned_weights