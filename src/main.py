from dataclasses import dataclass
from math import ceil
from typing import Dict

@dataclass
class Decision:
    allowed: bool
    remaining: int
    retry_after_ms: int


class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity: int = capacity
        self.refill_rate: float = refill_rate  # tokens per second
        self.buckets: Dict[str, float] = {}  # customer_id -> token count
        self.last_refill: Dict[str, int] = {}  # customer_id -> timestamp in ms

    def initialize_customer(self, customer_id: str, current_time_ms: int) -> None:
        self.buckets[customer_id] = float(self.capacity)
        self.last_refill[customer_id] = current_time_ms

    def refill_bucket(self, customer_id: str, current_time_ms: int) -> None:
        elapsed_ms = current_time_ms - self.last_refill[customer_id]
        tokens_to_add = (elapsed_ms / 1000.0) * self.refill_rate
        self.buckets[customer_id] = min(self.capacity, self.buckets[customer_id] + tokens_to_add)
        self.last_refill[customer_id] = current_time_ms

    def check(self, customer_id: str, current_time_ms: int) -> Decision:
        if customer_id not in self.buckets:
            self.initialize_customer(customer_id, current_time_ms)

        self.refill_bucket(customer_id, current_time_ms)

        current_tokens = self.buckets[customer_id]
        if current_tokens >= 1.0:
            self.buckets[customer_id] = current_tokens - 1.0
            return Decision(
                allowed=True,
                remaining=int(self.buckets[customer_id]),
                retry_after_ms=0,
            )

        tokens_needed = max(0.0, 1.0 - current_tokens)
        retry_after_ms = ceil((tokens_needed / self.refill_rate) * 1000)
        return Decision(
            allowed=False,
            remaining=int(self.buckets[customer_id]),
            retry_after_ms=retry_after_ms,
        )


