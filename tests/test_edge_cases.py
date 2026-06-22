from src.main import TokenBucketRateLimiter


def test_deny_when_bucket_empty():
    limiter = TokenBucketRateLimiter(capacity=100, refill_rate=10.0)
    for _ in range(100):
        limiter.check("customer1", current_time_ms=0)

    decision = limiter.check("customer1", current_time_ms=0)
    assert not decision.allowed
    assert decision.retry_after_ms > 0


def test_continuous_refill_fractional_tokens():
    limiter = TokenBucketRateLimiter(capacity=100, refill_rate=10.0)
    limiter.check("customer1", current_time_ms=0)

    decision = limiter.check("customer1", current_time_ms=50)
    assert decision.allowed
    assert decision.remaining == 98
