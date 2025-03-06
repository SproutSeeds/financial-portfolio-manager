import numpy as np
from jinja2 import Environment, FileSystemLoader
import datetime
import os
import shutil

def generate_report(name, assets, weights, risk_tolerance, goals, performance, comparison, correlation_matrix, high_corr_pairs, style_correlations, style_weights, risk_scores, portfolio_risk_score, recommendations, final_values):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report_template.html')
    report_data = {
        'name': name,
        'date': datetime.date.today().strftime("%B %d, %Y"),
        'assets': ', '.join(assets),
        'weights': ', '.join(map(str, weights)),
        'risk_tolerance': risk_tolerance,
        'goals': goals,
        'portfolio_risk_score': portfolio_risk_score,
        'risk_level': 'Low' if portfolio_risk_score < 4 else 'High' if portfolio_risk_score > 6 else 'Moderate',
        'risk_scores': risk_scores,
        'annualized_return': round(performance['annualized_return'] * 100, 2),
        'volatility': round(performance['volatility'] * 100, 2),
        'sharpe_ratio': round(performance['sharpe_ratio'], 2),
        'benchmark_annualized_return': round(comparison['benchmark_annualized_return'] * 100, 2),
        'benchmark_volatility': round(comparison['benchmark_volatility'] * 100, 2),
        'correlation_matrix': correlation_matrix.to_html(),
        'high_corr_pairs': high_corr_pairs,
        'style_correlations': style_correlations,
        'style_weights': {style: round(weight * 100, 2) for style, weight in style_weights.items()},
        'recommendations': recommendations,
        'monte_carlo_mean': round(np.mean(final_values), 2),
        'monte_carlo_std': round(np.std(final_values), 2),
        'cumulative_returns_plot': 'cumulative_returns.png',
        'correlation_heatmap': 'correlation_heatmap.png',
        'style_exposure_plot': 'style_exposure.png',
        'risk_gauge_plot': 'risk_gauge.png',
        'monte_carlo_plot': 'monte_carlo.png'
    }
    html_content = template.render(report_data)
    
    reports_dir = os.path.expanduser("~/financial_portfolio_manager_reports")
    os.makedirs(reports_dir, exist_ok=True)
    customer_dir = os.path.join(reports_dir, name.replace(" ", "_"))
    os.makedirs(customer_dir, exist_ok=True)
    
    report_filename = f"report_{name.replace(' ', '_')}_{datetime.date.today().strftime('%Y%m%d')}.html"
    report_path = os.path.join(customer_dir, report_filename)
    with open(report_path, 'w') as f:
        f.write(html_content)
    
    for img in ['cumulative_returns.png', 'correlation_heatmap.png', 'style_exposure.png', 'risk_gauge.png', 'monte_carlo.png']:
        shutil.copy(img, customer_dir)
    
    print(f"Report saved to {report_path}")