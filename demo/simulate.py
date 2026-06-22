import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.main import TokenBucketRateLimiter


def run_demo():
    limiter = TokenBucketRateLimiter(capacity=100, refill_rate=10.0)
    events = [
        ("customer1", 0),
        ("customer1", 100),
        ("customer1", 1000),
        ("customer1", 15000),
        ("customer1", 16000),
    ]

    for customer_id, timestamp in events:
        decision = limiter.check(customer_id, timestamp)
        print(
            f"time={timestamp}ms, customer={customer_id}, allowed={decision.allowed}, "
            f"remaining={decision.remaining}, retry_after_ms={decision.retry_after_ms}"
        )


if __name__ == "__main__":
    run_demo()


