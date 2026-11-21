#!/usr/bin/env python3
# example: python speed_test.py "https://grandtrain.ru/"
"""Measure sequential HTTP download performance over 10 requests."""

import argparse
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REQUEST_COUNT = 10
CHUNK_SIZE = 64 * 1024
TIMEOUT_SECONDS = 30

def process_request(url, number):
    try:
        elapsed, byte_count = download_once(url)
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        print(
            f"Request {number}/{REQUEST_COUNT} failed: {exc}",
            file=sys.stderr
        )
        return None

    print(
        f"Request {number:2}/{REQUEST_COUNT}: "
        f"{byte_count:,} bytes in {elapsed:.3f} s"
    )

    return elapsed, byte_count

def download_once(url: str) -> tuple[float, int]:
    """Download one complete response; return elapsed seconds and byte count."""
    request = Request(
        url,
        headers={"User-Agent": "internet-speed-test/1.0"},
    )
    started = time.perf_counter()
    downloaded = 0

    with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break
            downloaded += len(chunk)

    elapsed = time.perf_counter() - started
    return elapsed, downloaded

def get_args():
    parser = argparse.ArgumentParser(
        description="Download a URL 10 times sequentially and measure throughput."
    )
    parser.add_argument(
        "url",
        help="URL to download, for example https://example.com/image.jpg"
    )

    args = parser.parse_args()

    if not args.url.startswith(("http://", "https://")):
        parser.error("URL must start with http:// or https://")

    return args

def print_results(durations, total_bytes):
    total_time = sum(durations)
    average_time = total_time / len(durations)

    # Decimal megabits (1 Mbit = 1,000,000 bits)
    speed_mbps = (
        (total_bytes * 8 / total_time) / 1_000_000
        if total_time else 0.0
    )

    print("\n--- Results ---")
    print(f"Completed requests:       {len(durations)}")
    print(f"Average request time:     {average_time:.3f} s")
    print(
        f"Total downloaded:         {total_bytes:,} bytes "
        f"({total_bytes / 1_000_000:.3f} MB)"
    )
    print(f"Total download time:      {total_time:.3f} s")
    print(f"Average download speed:   {speed_mbps:.2f} Mbit/s")

def main() -> int:
    args = get_args()

    durations = []
    total_bytes = 0

    print(f"Target: {args.url}")
    print(f"Requests: {REQUEST_COUNT}\n")

    for number in range(1, REQUEST_COUNT + 1):
        result = process_request(args.url, number)

        if result is None:
            return 1

        elapsed, byte_count = result

        durations.append(elapsed)
        total_bytes += byte_count

    print_results(durations, total_bytes)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
