import yfinance as yf
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_data(assets):
    """
    Fetch historical adjusted closing prices for given assets.
    """
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=5 * 365)

    logging.info(f"Fetching data for assets: {assets} from {start_date} to {end_date}")

    try:
        data = yf.download(assets, start=start_date, end=end_date, auto_adjust=False)

        if data.empty:
            logging.error("Error: No data retrieved. Please check stock symbols and API status.")
            return None

        # Ensure 'Adj Close' column is present
        if 'Adj Close' in data.columns:
            return data['Adj Close']
        else:
            logging.warning("Warning: 'Adj Close' column is missing. Using 'Close' prices instead.")
            return data['Close'] if 'Close' in data.columns else None

    except Exception as e:
        logging.error(f"Failed to fetch data: {e}")
        return None

def fetch_benchmark_data(start_date, end_date, benchmark='SPY'):
    """
    Fetch historical adjusted closing prices for a benchmark index (default: SPY).
    """
    logging.info(f"Fetching benchmark data for {benchmark} from {start_date} to {end_date}")

    try:
        benchmark_data = yf.download(benchmark, start=start_date, end=end_date, auto_adjust=False)

        if benchmark_data.empty:
            logging.error("Error: No benchmark data retrieved. Check the symbol.")
            return None

        return benchmark_data['Adj Close'] if 'Adj Close' in benchmark_data.columns else benchmark_data['Close']

    except Exception as e:
        logging.error(f"Failed to fetch benchmark data: {e}")
        return None

def get_asset_info(asset):
    """
    Fetch company information for a given asset.
    """
    logging.info(f"Fetching asset info for {asset}")

    try:
        ticker = yf.Ticker(asset)
        info = ticker.info

        if not info:
            logging.warning(f"Warning: No information found for {asset}")
            return {}

        return info
    except Exception as e:
        logging.error(f"Failed to fetch asset info for {asset}: {e}")
        return {}