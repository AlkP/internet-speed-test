# Internet Speed Test

A small Python 3 command-line tool that downloads the same URL 10 times
sequentially, waits for each response body to finish, and reports the
average request time, total downloaded data, and average download speed.

## Requirements

- Python 3.9 or newer
- No third-party packages

## Run

```bash
python speed_test.py "https://grandtrain.ru/"
```

On some systems, use `python3` instead of `python`:

```bash
python3 speed_test.py "https://grandtrain.ru/"
```

The URL must use `http://` or `https://`. Each request has a 30-second
timeout. Requests are performed one after another, not concurrently.

## Output and units

The script prints the byte count and elapsed time for every request, then:

- **Average request time** — arithmetic mean of the 10 complete downloads, in seconds.
- **Total downloaded** — sum of response-body sizes, in bytes and decimal megabytes (MB).
- **Average download speed** — total downloaded bits divided by the sum of the 10 download times, in decimal megabits per second (Mbit/s).

Units use decimal prefixes: 1 MB = 1,000,000 bytes and 1 Mbit = 1,000,000 bits.
The reported speed is the average application-level throughput across these
downloads; it can be affected by server response time, caching, network
conditions, and HTTP overhead.

## Notes

- The response body is read fully in chunks, so large files are not loaded
  entirely into memory.
- The script counts response-body bytes, not HTTP headers.
- If any request fails, the script reports the error and exits with a
  non-zero status.
