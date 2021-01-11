import pypfopt
from pypfopt import (
    EfficientFrontier, HRPOpt,  objective_functions, 
    CLA, risk_models, expected_returns, plotting
)
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from pycoingecko import CoinGeckoAPI
from datetime import datetime
from pprint import pprint
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from sklearn.utils.extmath import weighted_mode
import yfinance as yf

from multiprocessing import Pool, Process, Manager

coingecko_client = CoinGeckoAPI()
manager = Manager()

return_model_dict = {
    "mean": expected_returns.mean_historical_return,
    "ema": expected_returns.ema_historical_return,
    "capm": expected_returns.capm_return,
}

risk_model_dict = {
    'sample_cov': risk_models.sample_cov,
    'semi_cov': risk_models.semicovariance,
    'exp_cov': risk_models.exp_cov,
    'min_cov_det': risk_models.min_cov_determinant,
    #'cov_shrink': risk_models.CovarianceShrinkage(df.cov(min_periods=100)),
    'ledoit_wolf': risk_models.risk_matrix,
    'ld_wolf_single': risk_models.risk_matrix,
    'oracle_approx': risk_models.risk_matrix,
}
 
def get_stocks_data(stocks_list, period):
    return yf.download(stocks_list, period=period)

def get_stocks_market_cap(stocks_list):
    def get_stock_mcap(d, stock):
        stock = yf.Ticker(stock)
        d[stock] = stock.info["marketCap"]
    mcaps = manager.dict()
    job = [Process(target=get_stocks_market_cap, args=(mcaps, i)) for i in stocks_list]
    [p.start() for p in job]
    [p.join() for p in job]
    return mcaps

def historical_value(data):

   stocks_data = get_stocks_data(
        stocks_list=data["coins_selected"], 
        period=data["period"],
    )
   stocks_price_matrix_df = stocks_data["Adj Close"]
   gamma = data["gamma"]    
   capital = data["capital"]
   initial_weights = np.array(
       [1/len(stocks_price_matrix_df.columns)] * len(stocks_price_matrix_df.columns)
   )
   broker_fees = 0.001
   risk_free_rate = data["risk_free_rate"]
   weight_bounds = (0,1)
   if data["short_selling"]:
       weight_bounds = (-1,1)

   e_r = data["returns_choice"]
   # Default is mean historical value
   return_model = expected_returns.mean_historical_return(stocks_price_matrix_df)
   if e_r == "ema_historical":
       return_model = expected_returns.ema_historical_return(stocks_price_matrix_df)
   elif e_r == "capm_returns":
       return_model = expected_returns.capm_return(stocks_price_matrix_df)

   r_c = data["risk_choice"]
   # Default is sample covariance
   risk_model = risk_models.sample_cov(stocks_price_matrix_df)
   if r_c == "semi covariance":
       risk_model = risk_models.semicovariance(stocks_price_matrix_df)
   elif r_c == "exponential covariance":
       risk_model = risk_models.exp_cov(stocks_price_matrix_df)
   elif r_c == "minimum determinant covariance":
       risk_model = risk_models.min_cov_determinant(stocks_price_matrix_df)
   #elif r_c == "covariance shrinkage":
   #    risk = risk_models.CovarianceShrinkage(stocks_price_matrix_df.cov(min_periods=15))
   elif r_c == "ledoit-wolf method":
       risk_model = risk_models.risk_matrix(prices=stocks_price_matrix_df, method='ledoit_wolf')
       #S = risk_models.risk_matrix(prices=df, method='ledoit_wolf_single_factor')
   elif r_c == "oracle approximation":
       risk_model = risk_models.risk_matrix(prices=stocks_price_matrix_df, method='oracle_approximating')
   

   efficient_frontier = EfficientFrontier(
       return_model, 
       risk_model, 
       weight_bounds=weight_bounds, 
       gamma=gamma
   )
   efficient_frontier.add_objective(
       objective_functions.transaction_cost, 
       w_prev=initial_weights, 
       k=broker_fees
   ) 
   efficient_frontier.add_objective(
       objective_functions.L2_reg, 
       gamma=gamma
   )  

   objectif = data["objectif"]
   efficient_frontier.min_volatility()
   if objectif == "max_sharpe":
       efficient_frontier.max_sharpe()
   elif objectif == "quadratic_utility":
       efficient_frontier.max_quadratic_utility()
   elif objectif == "efficient_risk":
       efficient_frontier.min_efficient_risk(0.5)
   elif objectif == "efficient_return":
       efficient_frontier.min_efficient_return(0.5)

   cleaned_weights = efficient_frontier.clean_weights()
   portfolio_performance = efficient_frontier.portfolio_performance(
       verbose=False, 
       risk_free_rate=risk_free_rate
   ) 

   latest_prices = get_latest_prices(stocks_price_matrix_df)
   discrete_allocation = DiscreteAllocation(
       cleaned_weights, 
       latest_prices, 
       total_portfolio_value=capital
   )
   allocation, leftover = discrete_allocation.lp_portfolio()
   result = {}
   return {
       "return": portfolio_performance[0],
       "risk": portfolio_performance[1],
       "sharpe ratio": portfolio_performance[2],
       "allocation": allocation,
       "leftover": leftover,
       "cleaned_weights": cleaned_weights,
   }

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





def hrpopt(data):

   stocks_data = get_stocks_data(
        stocks_list=data["coins_selected"], 
        period=data["period"],
    )
   stocks_price_matrix_df = stocks_data["Adj Close"]
   capital = data["capital"]
   risk_free_rate = data["risk_free_rate"]

   risk_model = risk_models.risk_matrix(prices=stocks_price_matrix_df, method='oracle_approximating')
   
   efficient_frontier = HRPOpt(stocks_price_matrix_df, risk_model)
   # Is this really useful ?
   raw_weights = efficient_frontier.optimize('single')

   cleaned_weights = efficient_frontier.clean_weights()
   portfolio_performance = efficient_frontier.portfolio_performance(
       verbose=False, 
       risk_free_rate=risk_free_rate
   ) 

   latest_prices = get_latest_prices(stocks_price_matrix_df)
   discrete_allocation = DiscreteAllocation(
       cleaned_weights, 
       latest_prices, 
       total_portfolio_value=capital
   )
   allocation, leftover = discrete_allocation.lp_portfolio()
   result = {}
   return {
       "return": portfolio_performance[0],
       "risk": portfolio_performance[1],
       "sharpe ratio": portfolio_performance[2],
       "allocation": allocation,
       "leftover": leftover,
       "cleaned_weights": cleaned_weights,
   }

