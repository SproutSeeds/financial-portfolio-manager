import pandas as pd
import numpy as np
import datetime
from .data_fetcher import fetch_data, fetch_benchmark_data, get_asset_info

def calculate_performance(data, weights):
    weights = np.array(weights)
    daily_returns = data.pct_change().dropna()
    portfolio_daily_returns = daily_returns.dot(weights)
    cumulative_returns = (1 + portfolio_daily_returns).cumprod()
    annualized_return = (cumulative_returns.iloc[-1]) ** (252 / len(cumulative_returns)) - 1
    volatility = portfolio_daily_returns.std() * np.sqrt(252)
    sharpe_ratio = (annualized_return - 0.02) / volatility
    return {
        'cumulative_returns': cumulative_returns,
        'annualized_return': annualized_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio
    }

def compare_to_benchmark(data, weights, benchmark='SPY'):
    benchmark_data = fetch_benchmark_data(data.index[0], data.index[-1], benchmark)
    benchmark_daily_returns = benchmark_data.pct_change().dropna()
    benchmark_cumulative_returns = (1 + benchmark_daily_returns).cumprod()
    benchmark_annualized_return = (benchmark_cumulative_returns.iloc[-1]) ** (252 / len(benchmark_cumulative_returns)) - 1
    benchmark_volatility = benchmark_daily_returns.std() * np.sqrt(252)
    portfolio_performance = calculate_performance(data, weights)
    return {
        'portfolio_cumulative_returns': portfolio_performance['cumulative_returns'],
        'benchmark_cumulative_returns': benchmark_cumulative_returns,
        'portfolio_annualized_return': portfolio_performance['annualized_return'],
        'benchmark_annualized_return': benchmark_annualized_return,
        'portfolio_volatility': portfolio_performance['volatility'],
        'benchmark_volatility': benchmark_volatility
    }

def classify_investment_style(assets):
    style_classification = {}
    for asset in assets:
        info = get_asset_info(asset)
        pe_ratio = info.get('trailingPE', float('inf'))
        dividend_yield = info.get('dividendYield', 0) * 100
        sector = info.get('sector', '').lower()

        if 'bond' in asset.lower() or dividend_yield > 4:
            style = 'Income'
        elif pe_ratio > 25 and dividend_yield < 1:
            style = 'Growth'
        else:
            style = 'Value'
        
        style_classification[asset] = style
    return style_classification

def calculate_dynamic_risk_scores(assets, benchmark='SPY'):
    risk_scores = {}
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=5*365)
    
    benchmark_data = fetch_benchmark_data(start_date, end_date, benchmark)
    benchmark_returns = benchmark_data.pct_change().dropna()
    
    for asset in assets:
        info = get_asset_info(asset)
        beta = info.get('beta', 1.0)
        
        if beta < 0.5:
            risk_score = 1 + (beta / 0.5)
        elif beta < 1.0:
            risk_score = 2 + (beta - 0.5) * (3 / 0.5)
        elif beta < 1.5:
            risk_score = 5 + (beta - 1.0) * (3 / 0.5)
        else:
            risk_score = 8 + (beta - 1.5) * (2 / 1.0)
            if risk_score > 10:
                risk_score = 10
        
        risk_scores[asset] = round(risk_score, 2)
    return risk_scores

def calculate_portfolio_risk_score(risk_scores, weights):
    portfolio_risk_score = 0
    for asset, weight in zip(risk_scores.keys(), weights):
        portfolio_risk_score += weight * risk_scores[asset]
    return round(portfolio_risk_score, 2)

def get_sector_exposure(assets):
    sector_exposure = {}
    for asset in assets:
        info = get_asset_info(asset)
        sector = info.get('sector', 'Unknown')
        sector_exposure[asset] = sector
    return sector_exposure

def analyze_diversification(data, style_classification):
    daily_returns = data.pct_change().dropna()
    correlation_matrix = daily_returns.corr()
    high_corr_pairs = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            if abs(correlation_matrix.iloc[i,j]) > 0.8:
                high_corr_pairs.append((correlation_matrix.columns[i], correlation_matrix.columns[j], correlation_matrix.iloc[i,j]))

    style_correlations = {}
    styles = set(style_classification.values())
    for style1 in styles:
        for style2 in styles:
            if style1 >= style2:
                continue
            assets_style1 = [asset for asset, style in style_classification.items() if style == style1]
            assets_style2 = [asset for asset, style in style_classification.items() if style == style2]
            if not assets_style1 or not assets_style2:
                continue
            returns_style1 = daily_returns[assets_style1].mean(axis=1)
            returns_style2 = daily_returns[assets_style2].mean(axis=1)
            style_corr = returns_style1.corr(returns_style2)
            style_correlations[f"{style1}-{style2}"] = style_corr

    return correlation_matrix, high_corr_pairs, style_correlations

def monte_carlo_simulation(data, weights, num_simulations=1000, num_days=252):
    daily_returns = data.pct_change().dropna()
    mean_returns = daily_returns.mean()
    cov_matrix = daily_returns.cov()
    sim_returns = np.random.multivariate_normal(mean_returns, cov_matrix, (num_days, num_simulations))
    portfolio_sim_returns = np.dot(sim_returns, weights)
    portfolio_values = np.cumprod(1 + portfolio_sim_returns, axis=0)
    final_values = portfolio_values[-1, :]
    return final_values