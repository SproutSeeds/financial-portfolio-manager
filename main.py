from financial_portfolio_manager_analyzer.data_fetcher import fetch_data
from financial_portfolio_manager_analyzer.portfolio_analyzer import calculate_performance, compare_to_benchmark, classify_investment_style, calculate_dynamic_risk_scores, calculate_portfolio_risk_score, analyze_diversification, monte_carlo_simulation
from financial_portfolio_manager_analyzer.recommender import generate_recommendations
from financial_portfolio_manager_analyzer.visualizer import create_cumulative_returns_plot, create_correlation_heatmap, create_style_exposure_pie, create_risk_gauge, create_monte_carlo_histogram
from financial_portfolio_manager_analyzer.report_generator import generate_report

def get_user_input():
    print("Welcome to Financial Portfolio Manager Portfolio Analyzer")
    name = input("Enter customer's name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name = input("Enter customer's name: ").strip()

    while True:
        assets = input("Enter portfolio assets (comma-separated, e.g., AAPL,GOOG,SPY): ").strip()
        assets = [asset.strip().upper() for asset in assets.split(',')]
        if len(assets) < 1 or '' in assets:
            print("Please enter at least one valid asset.")
            continue
        try:
            test_data = fetch_data(assets)
            if test_data.empty or test_data.isna().all().all():
                raise ValueError("No valid data for these assets.")
            break
        except Exception as e:
            print(f"Error with assets: {e}. Please enter valid stock symbols.")

    while True:
        try:
            weights = list(map(float, input("Enter weights (comma-separated, should sum to 1): ").split(',')))
            if len(weights) != len(assets):
                print(f"Number of weights ({len(weights)}) must match number of assets ({len(assets)}).")
                continue
            if any(w <= 0 for w in weights):
                print("Weights must be positive.")
                continue
            if abs(sum(weights) - 1) > 0.01:
                print("Weights do not sum to 1. Please re-enter.")
                continue
            break
        except ValueError:
            print("Weights must be numeric values.")

    while True:
        try:
            risk_tolerance = int(input("Enter risk tolerance (1-10): "))
            if risk_tolerance < 1 or risk_tolerance > 10:
                print("Risk tolerance must be between 1 and 10.")
                continue
            break
        except ValueError:
            print("Risk tolerance must be an integer.")

    goals = input("Enter financial goals (e.g., retirement, wealth accumulation): ").strip()
    while not goals:
        print("Goals cannot be empty.")
        goals = input("Enter financial goals: ").strip()

    return name, assets, weights, risk_tolerance, goals

def main():
    name, assets, weights, risk_tolerance, goals = get_user_input()
    
    data = fetch_data(assets)
    
    style_classification = classify_investment_style(assets)
    risk_scores = calculate_dynamic_risk_scores(assets)
    portfolio_risk_score = calculate_portfolio_risk_score(risk_scores, weights)
    performance = calculate_performance(data, weights)
    comparison = compare_to_benchmark(data, weights)
    correlation_matrix, high_corr_pairs, style_correlations = analyze_diversification(data, style_classification)
    
    recommendations, style_weights = generate_recommendations(risk_tolerance, performance['volatility'], comparison['benchmark_volatility'], high_corr_pairs, style_correlations, style_classification, weights, goals, assets, portfolio_risk_score)
    
    create_cumulative_returns_plot(data, weights)
    create_correlation_heatmap(data)
    create_style_exposure_pie(style_weights)
    create_risk_gauge(portfolio_risk_score, risk_tolerance)
    final_values = monte_carlo_simulation(data, weights)
    create_monte_carlo_histogram(final_values)
    
    generate_report(name, assets, weights, risk_tolerance, goals, performance, comparison, correlation_matrix, high_corr_pairs, style_correlations, style_weights, risk_scores, portfolio_risk_score, recommendations, final_values)
    print("Report generated successfully.")

if __name__ == '__main__':
    main()