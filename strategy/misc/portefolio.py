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
from sklearn.utils.extmath import weighted_mode

def ici(data):

    client = CoinGeckoAPI()

    ### Configuration
    from_date_str = "01-01-2019"
    to_date_str = "01-11-2020"

    from_date = datetime.strptime(from_date_str, '%d-%m-%Y')
    to_date = datetime.strptime(to_date_str, '%d-%m-%Y')

    coins_list = data["coins_selected"]

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
            tmp.append({
                "date": pd.Timestamp(flat_timestamp[i], unit='ms', tz="UTC"),
                "price": flat_price[i], 
                "total_volume": flat_total_volume[i], 
                "market_cap": flat_market_cap[i],
                "coin_name": coin,
            })
        df = pd.DataFrame(tmp, columns=("date", "price", "total_volume","market_cap", "coin_name"))
        df.set_index(["date"])
        tickers[coin] = df

    ### Calcul des Perfs/Volatilité Weekly/Daily

    for coin in coins_list:
        _ = tickers[coin]
        _["daily_perfs"] = _["price"].pct_change()
        _["cum_daily_perfs"] = _["daily_perfs"].cumsum()
        _["weekly_perfs"] = _.loc[(_["date"].dt.day_name() == 'Monday')]['price'].pct_change()
        _["cum_weekly_perfs"] = _["weekly_perfs"].cumsum()
        #print(_.loc[(_["date"].dt.day_name() == 'Monday')]['price'].pct_change())
        #_["weekly_perfs"] = _.lo
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

    # Test avec les différent join pour les tickers où les dimensions de prix ne matchent pas
    # min_periods dans la covar pour enlever si il n'y a pas assez de data
    price_matrix = pd.concat([tickers[coin]["price"].rename(coin) for coin in coins_list], axis=1, join='inner')
    #price_matrix.cov()
    #price_matrix.reset_index(drop=True, inplace=True)
    # pour rajouter les date au dataframe de prix
    #date_price_matrix = pd.concat([tickers[coin]["date"], price_matrix], axis=1, join='inner')
    #df = date_price_matrix
    df = price_matrix


    e_r = data["returns_choice"]
    # Default is mean historical value
    mu = expected_returns.mean_historical_return(df)
    if e_r == "ema_historical":
        mu = expected_returns.ema_historical_return(df)
    elif e_r == "capm_returns":
        mu = expected_returns.capm_return(df)

    r_c = data["risk_choice"]
    # Default is sample covariance
    S = risk_models.sample_cov(df)
    if r_c == "semi covariance":
        S = risk_models.semicovariance(df)
    elif r_c == "exponential covariance":
        S = risk_models.exp_cov(df)
    elif r_c == "minimum determinant covariance":
        S = risk_models.min_cov_determinant(df)
    elif r_c == "covariance shrinkage":
        S = risk_models.CovarianceShrinkage(df.cov(min_periods=15))
    elif r_c == "ledoit-wolf method":
        S = risk_models.risk_matrix(prices=df, method='ledoit_wolf')
        #S = risk_models.risk_matrix(prices=df, method='ledoit_wolf_single_factor')
    elif r_c == "oracle approximation":
        S = risk_models.risk_matrix(prices=df, method='oracle_approximating')

    #mu.plot.barh(figsize=(10,5))
    #plotting.plot_covariance(S, plot_correlation=True)

    # Pretend that you started with a default-weight allocation
    initial_weights = np.array([1/len(tickers)] * len(tickers))

    w_b = data["short_selling"]
    weight_bounds = (0, 1)
    if w_b:
        weight_bounds = (-1, 1)

    gamma = data["gamma"]
    ef = EfficientFrontier(mu, S, weight_bounds=weight_bounds, gamma=gamma)
    ef.add_objective(objective_functions.transaction_cost, w_prev=initial_weights, k=0.001) # 1% broker commission
    ef.add_objective(objective_functions.L2_reg, gamma=gamma)  # default is gamma=1

    obj = data["objectif"]
    ef.min_volatility()
    if obj == "max_sharpe":
        ef.max_sharpe()
    elif obj == "quadratic_utility":
        ef.max_quadratic_utility()
    elif obj == "efficient_risk":
        ef.min_efficient_risk(0.5)
    elif obj == "efficient_return":
        ef.min_efficient_return(0.5)

    cleaned_weights = ef.clean_weights()

    risk_free_rate = data["risk_free_rate"]
    ef.portfolio_performance(verbose=True, risk_free_rate=risk_free_rate)

    latest_prices = get_latest_prices(df)
    total_portfolio_value = data["capital"]
    short_ratio = data["short_ratio"]
    da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value=total_portfolio_value, short_ratio=short_ratio)

    allocation, leftover = da.lp_portfolio()
    #allocation, leftover = da.greedy_portfolio()
    #print("Discrete allocation:", allocation)
    #print("Funds remaining: ${:.2f}".format(leftover))

    return allocation, cleaned_weights