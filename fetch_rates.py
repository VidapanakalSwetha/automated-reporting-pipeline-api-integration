import requests
import json
import logging
from datetime import datetime
from config import API_KEY

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_rates():
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            raise ValueError(f"API returned failure: {data}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/raw/rates_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        logging.info(f"Pull successful, saved to {filename}")
        print(f"Saved: {filename}")

    except requests.exceptions.Timeout:
        logging.error("Pull failed: request timed out")
    except requests.exceptions.ConnectionError:
        logging.error("Pull failed: no internet/connection error")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Pull failed: HTTP error - {e}")
    except Exception as e:
        logging.error(f"Pull failed: unexpected error - {e}")

if __name__ == "__main__":
    fetch_rates()