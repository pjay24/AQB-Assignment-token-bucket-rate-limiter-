# Implementation Notes

## What is implemented

- `src/main.py`
  - `Decision` dataclass with `allowed`, `remaining`, and `retry_after_ms`.
  - `TokenBucketRateLimiter` class with:
    - `capacity` and `refill_rate` configured in the constructor.
    - `buckets` mapping customer IDs to floating-point token counts.
    - `last_refill` mapping customer IDs to the last timestamp in milliseconds.
  - `initialize_customer(customer_id, current_time_ms)` to start new customers with a full bucket and store the initial timestamp.
  - `refill_bucket(customer_id, current_time_ms)` to compute elapsed time, add fractional tokens based on `refill_rate`, cap at `capacity`, and update the timestamp.
  - `check(customer_id, current_time_ms)` to initialize unknown customers, refill before request processing, consume one token if available, and return the correct `Decision`.

## How it works

- New customers begin with `capacity` tokens.
- Each request uses the provided `current_time_ms` in milliseconds.
- The bucket is refilled lazily on each request using the elapsed time since the previous request.
- Refill is computed as `(elapsed_ms / 1000) * refill_rate`, allowing fractional tokens to accumulate.
- The bucket is capped at `capacity` after refill.
- If at least one token is available, the request is allowed and one token is consumed.
- If the bucket is empty, `retry_after_ms` is calculated as the milliseconds needed to reach one token, using `ceil(...)` to avoid underestimating the wait.
- Customer state is maintained independently by customer ID.

## Tests and validation

- `tests/test_scenario.py` contains the main end-to-end and scenario-based tests.
- `tests/test_edge_cases.py` covers edge conditions like fractional refill and empty-bucket denial.
- Demo script `demo/simulate.py` runs a sample request sequence and prints outcomes.
- Verified with `python3 -m pytest -q tests` in a local virtual environment, yielding `5 passed`.

## How to run

- Run the demo:
  - `python3 demo/simulate.py`

## Notes

- `src/__init__.py` was added to make `src` importable.
- A local virtual environment `.venv` was created for test execution.
- No `utils` directory was included, as requested.
