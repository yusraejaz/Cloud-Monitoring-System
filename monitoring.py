import json
import csv
import time
import logging
import requests

from pathlib import Path
from datetime import datetime
from time import perf_counter

BASE_DIR = Path(__file__).parent

CONFIG_FILE = BASE_DIR / "config.json"
LOG_FILE = BASE_DIR / "logs" / "monitoring.log"
REPORT_FILE = BASE_DIR / "reports" / "uptime_report.csv"

LOG_FILE.parent.mkdir(exist_ok=True)
REPORT_FILE.parent.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = json.load(file)

URLS = config["urls"]
INTERVAL = config["check_interval_seconds"]
TIMEOUT = config["timeout_seconds"]
LATENCY_THRESHOLD = config["latency_threshold_ms"]
ALERT_ON_FAILURE = config["alert_on_failure"]

FIELDS = [
    "timestamp",
    "url",
    "http_status",
    "latency_ms",
    "status",
    "uptime_percent"
]

if not REPORT_FILE.exists() or REPORT_FILE.stat().st_size == 0:
    with open(REPORT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()

def check_website(url):
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    status_code = "N/A"
    latency_ms = 0

    try:
        start_time = perf_counter()
        response = requests.get(url, timeout=TIMEOUT)
        latency_ms = round((perf_counter() - start_time) * 1000, 2)
        status_code = response.status_code

        if response.status_code < 400:
            status = "UP"
        else:
            status = "DOWN"

    except requests.RequestException as error:
        status = "DOWN"
        print(f"ERROR: {error}")
        logging.error("%s - %s", url, error)

    if status == "DOWN":
        print(f"ALERT: {url} is DOWN!")
        if ALERT_ON_FAILURE:
            logging.warning("%s is DOWN", url)

    elif latency_ms > LATENCY_THRESHOLD:
        print(f"SLOW WARNING: {url} response time is {latency_ms} ms")

    else:
        print(f"UP: {url} | Status: {status_code} | Latency: {latency_ms} ms")

    with open(REPORT_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writerow({
            "timestamp": timestamp,
            "url": url,
           "http_status": status_code,
            "latency_ms": latency_ms,
            "status": status,
            "uptime_percent": ""
        })

    with open(REPORT_FILE, "r", newline="", encoding="utf-8") as file:
        records = [
            row for row in csv.DictReader(file)
            if row["url"] == url
        ]

    total_checks = len(records)

    successful_checks = sum(
        1 for row in records
        if row["status"] == "UP"
    )

    if total_checks > 0:
        uptime = round((successful_checks / total_checks) * 100, 2)
    else:
        uptime = 0.0

    with open(REPORT_FILE, "a", newline="", encoding="utf-8") as file:
        pass

    print(f"Uptime: {uptime}% ({successful_checks}/{total_checks} checks)")
    logging.info(
        "%s | Status: %s | HTTP: %s | Latency: %s ms | Uptime: %s%%",
        url, status, status_code, latency_ms, uptime
    )


def main():
    print("CLOUD MONITORING SYSTEM STARTED")
    print("Press CTRL+C to stop monitoring.")

    try:
        while True:
            print("\n--- New Monitoring Cycle ---")

            for url in URLS:
                check_website(url)

            print(f"\nNext check in {INTERVAL} seconds...")
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
        logging.info("Monitoring stopped by user.")


if __name__ == "__main__":
    main()
