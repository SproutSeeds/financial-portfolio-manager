import pandas as pd
from .portfolio_analyzer import get_sector_exposure

def generate_recommendations(risk_tolerance, portfolio_volatility, benchmark_volatility, high_corr_pairs, style_correlations, style_classification, weights, goals, assets, portfolio_risk_score):
    recommendations = []

    risk_mismatch_threshold = 2
    if portfolio_risk_score > risk_tolerance + risk_mismatch_threshold:
        recommendations.append(f"Your portfolio risk score ({portfolio_risk_score}) is significantly higher than your risk tolerance ({risk_tolerance}). Consider reducing exposure to high-risk assets and adding more stable investments like bonds or dividend stocks.")
    elif portfolio_risk_score < risk_tolerance - risk_mismatch_threshold:
        recommendations.append(f"Your portfolio risk score ({portfolio_risk_score}) is significantly lower than your risk tolerance ({risk_tolerance}). You might consider adding higher-risk assets like growth stocks to potentially increase returns.")

    if risk_tolerance < 4 and portfolio_volatility > benchmark_volatility.iloc[0]:
        recommendations.append("Your portfolio is more volatile than the benchmark (S&P 500). Consider shifting to more conservative investments, such as bonds or dividend-paying stocks.")
    elif risk_tolerance > 7 and portfolio_volatility < benchmark_volatility.iloc[0]:
        recommendations.append("Your portfolio is less volatile than the benchmark (S&P 500). If seeking higher returns, you might consider adding growth stocks or ETFs in emerging markets.")

    if high_corr_pairs:
        pairs_text = ", ".join([f"{pair[0]} and {pair[1]} (correlation: {pair[2]:.2f})" for pair in high_corr_pairs])
        recommendations.append(f"Your portfolio has highly correlated assets ({pairs_text}), which may increase risk. Consider diversifying into different sectors or asset classes.")

    style_weights = {'Growth': 0, 'Value': 0, 'Income': 0, 'Unknown': 0}
    for asset, weight in zip(assets, weights):
        style = style_classification.get(asset, 'Unknown')
        style_weights[style] += weight
    dominant_style = max(style_weights, key=style_weights.get)
    dominant_style_weight = style_weights[dominant_style]

    if dominant_style == 'Growth' and dominant_style_weight > 0.6 and risk_tolerance < 5:
        recommendations.append(f"Your portfolio is heavily weighted toward Growth assets ({dominant_style_weight:.0%}), which are typically higher risk. Given your risk tolerance ({risk_tolerance}), consider adding Value or Income assets like dividend stocks or bonds.")
    elif dominant_style == 'Income' and dominant_style_weight > 0.6 and risk_tolerance > 7:
        recommendations.append(f"Your portfolio is heavily weighted toward Income assets ({dominant_style_weight:.0%}), which are typically lower risk. Given your risk tolerance ({risk_tolerance}), you might consider adding Growth stocks to increase potential returns.")

    for style_pair, corr in style_correlations.items():
        if abs(corr) > 0.8:
            recommendations.append(f"Your {style_pair} assets are highly correlated (correlation: {corr:.2f}), which may increase risk. Consider diversifying within these styles.")
        elif abs(corr) < 0.3:
            recommendations.append(f"Your {style_pair} assets have low correlation (correlation: {corr:.2f}), which is good for diversification.")

    sector_exposure = get_sector_exposure(assets)
    sector_counts = pd.Series(sector_exposure.values()).value_counts()
    dominant_sector = sector_counts.idxmax()
    dominant_sector_weight = sector_counts[dominant_sector] / len(assets)
    if dominant_sector_weight > 0.5:
        recommendations.append(f"Your portfolio is heavily concentrated in the {dominant_sector} sector ({dominant_sector_weight:.0%} of assets). To reduce sector-specific risk, consider diversifying into other sectors like healthcare or consumer staples.")

    if 'retirement' in goals.lower():
        recommendations.append("For retirement planning, ensure your portfolio includes stable, income-generating assets like bonds or dividend stocks, and aligns with your time horizon and risk tolerance.")
    elif 'wealth accumulation' in goals.lower():
        recommendations.append("For wealth accumulation, consider a balanced mix of growth stocks and ETFs, and review your portfolio annually to rebalance.")

    if not recommendations:
        recommendations.append("Your portfolio appears well-balanced for your risk tolerance and goals. Continue monitoring market conditions and rebalance as needed.")

    return recommendations, style_weights