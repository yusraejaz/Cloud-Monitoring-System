# Cloud Monitoring System

A Python-based automated website monitoring system that checks website availability, measures response time, tracks HTTP status codes, and records uptime reports.

## Features
- Automated website health checks
- HTTP status code monitoring
- Response time measurement in milliseconds
- Uptime percentage tracking
- Failure and latency alerts
- CSV-based historical reports
- Monitoring activity logs

## Technologies Used
- Python
- Requests Library
- JSON
- CSV
- Git and GitHub

## Installation

Install the required Python package:

pip install -r requirements.txt

## Configuration

Edit config.json to configure:
- Website URLs
- Check interval
- Request timeout
- Latency threshold
- Failure alert settings

## Run the Project

python monitoring.py

Press CTRL+C to stop monitoring.

## Monitoring Report

Monitoring results are saved in:

reports/uptime_report.csv

The report includes timestamps, URLs, HTTP status codes, latency, and website status.

## Test Results

Google and GitHub were tested successfully. Both returned HTTP 200 during the initial monitoring test.

## Author

Yusra Ejaz