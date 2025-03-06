import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from .data_fetcher import fetch_benchmark_data

def create_cumulative_returns_plot(data, weights, benchmark='SPY'):
    weights = np.array(weights)
    daily_returns = data.pct_change().dropna()
    portfolio_daily_returns = daily_returns.dot(weights)
    portfolio_cumulative = (1 + portfolio_daily_returns).cumprod()
    
    benchmark_data = fetch_benchmark_data(data.index[0], data.index[-1], benchmark)
    benchmark_cumulative = (1 + benchmark_data.pct_change()).cumprod()
    
    plt.figure(figsize=(10,6))
    plt.plot(portfolio_cumulative, label='Portfolio')
    plt.plot(benchmark_cumulative, label=benchmark)
    plt.title('Cumulative Returns')
    plt.legend()
    plt.savefig('cumulative_returns.png')
    plt.close()

def create_correlation_heatmap(data):
    daily_returns = data.pct_change().dropna()
    correlation_matrix = daily_returns.corr()
    plt.figure(figsize=(8,6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Asset Correlation Matrix')
    plt.savefig('correlation_heatmap.png')
    plt.close()
    return correlation_matrix

def create_style_exposure_pie(style_weights):
    plt.figure(figsize=(8,6))
    labels = [f"{style} ({weight:.0%})" for style, weight in style_weights.items() if weight > 0]
    sizes = [weight for weight in style_weights.values() if weight > 0]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Portfolio Allocation by Investment Style')
    plt.savefig('style_exposure.png')
    plt.close()

def create_risk_gauge(portfolio_risk_score, risk_tolerance):
    fig, ax = plt.subplots(figsize=(8, 4), subplot_kw={'aspect': 'equal'})
    
    angles = np.linspace(np.pi, 0, 181)
    radius = 1
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    
    ax.fill_between(x, y, color='lightgray', alpha=0.3)
    
    low_angles = np.linspace(np.pi, 2*np.pi/3, 61)
    mod_angles = np.linspace(2*np.pi/3, np.pi/3, 61)
    high_angles = np.linspace(np.pi/3, 0, 61)
    ax.fill_between(radius * np.cos(low_angles), radius * np.sin(low_angles), color='green', alpha=0.5)
    ax.fill_between(radius * np.cos(mod_angles), radius * np.sin(mod_angles), color='yellow', alpha=0.5)
    ax.fill_between(radius * np.cos(high_angles), radius * np.sin(high_angles), color='red', alpha=0.5)
    
    score_angle = np.pi - (portfolio_risk_score - 1) * (np.pi / 9)
    ax.plot([0, radius * np.cos(score_angle)], [0, radius * np.sin(score_angle)], color='black', linewidth=3, label='Portfolio Risk Score')
    
    tolerance_angle = np.pi - (risk_tolerance - 1) * (np.pi / 9)
    ax.plot([0, radius * np.cos(tolerance_angle)], [0, radius * np.sin(tolerance_angle)], color='blue', linewidth=3, linestyle='--', label='Risk Tolerance')
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('Portfolio Risk Score vs. Risk Tolerance')
    ax.legend()
    
    ax.text(-1.2, 0, 'Low', color='green', fontsize=10)
    ax.text(0, 0, 'Moderate', color='black', fontsize=10)
    ax.text(1.2, 0, 'High', color='red', fontsize=10)
    
    plt.savefig('risk_gauge.png', bbox_inches='tight')
    plt.close()

def create_monte_carlo_histogram(final_values):
    plt.figure(figsize=(10,6))
    plt.hist(final_values, bins=50)
    plt.title('Distribution of Portfolio Values after 1 Year')
    plt.xlabel('Portfolio Value')
    plt.ylabel('Frequency')
    plt.savefig('monte_carlo.png')
    plt.close()