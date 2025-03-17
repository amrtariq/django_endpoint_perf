# Endpoint Performance Comparison

A Python script to compare the performance of different API endpoints by measuring response times, record counts, and query efficiency.

## Features

- Tests multiple API endpoints for performance metrics
- Measures average, minimum, and maximum response times
- Calculates standard deviation of response times
- Tracks number of records processed
- Monitors query counts per request
- Supports both regular and paginated (SSE) endpoints

## Setup

1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install requests
   ```

## Usage

1. Configure the endpoints to test in `compare_performance.py`:
   ```python
   endpoints = [
       f"{base_url}values/",
       f"{base_url}threaded/",
       f"{base_url}row/",
       f"{base_url}paginated/"
   ]
   ```

2. Run the script:
   ```bash
   python compare_performance.py
   ```

3. View the performance comparison summary in the console output

## Output Format

The script generates a formatted table with the following metrics for each endpoint:
- Average response time
- Minimum response time
- Maximum response time
- Standard deviation
- Number of records processed
- Average queries per request

## Notes

- The script automatically handles both regular REST endpoints and Server-Sent Events (SSE) endpoints
- For SSE endpoints, it tracks individual chunks and aggregates the data
- Response times are measured in seconds