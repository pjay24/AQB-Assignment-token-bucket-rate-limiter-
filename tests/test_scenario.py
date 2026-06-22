from src.main import TokenBucketRateLimiter


def test_example_scenario():
    limiter = TokenBucketRateLimiter(capacity=100, refill_rate=10.0)
    decision = limiter.check("customer1", current_time_ms=0)

    assert decision.allowed
    assert decision.remaining == 99
    assert decision.retry_after_ms == 0

    decision = limiter.check("customer1", current_time_ms=1000)
    assert decision.allowed
    assert decision.remaining == 99
    assert decision.retry_after_ms == 0


def test_refill_after_delay():
    limiter = TokenBucketRateLimiter(capacity=100, refill_rate=10.0)
    limiter.check("customer1", current_time_ms=0)
    limiter.check("customer1", current_time_ms=0)

    decision = limiter.check("customer1", current_time_ms=5000)
    assert decision.allowed
    assert decision.remaining == 99
    assert decision.retry_after_ms == 0


def test_token_bucket_problem_end_to_end():
    limiter = TokenBucketRateLimiter(capacity=100, refill_rate=10.0)

    # 1. first request succeeds and bucket starts full
    decision = limiter.check("customerA", current_time_ms=0)
    assert decision.allowed
    assert decision.remaining == 99
    assert decision.retry_after_ms == 0

    # 2. continuous refill after 1.5 seconds
    decision = limiter.check("customerA", current_time_ms=1500)
    assert decision.allowed
    assert decision.remaining == 99
    assert decision.retry_after_ms == 0

    # 3. capacity remains capped at 100 even with long delay
    limiter.check("customerB", current_time_ms=0)
    limiter.check("customerB", current_time_ms=0)
    decision = limiter.check("customerB", current_time_ms=20000)
    assert decision.allowed
    assert decision.remaining == 99

    # 4. retry time calculation when bucket is empty
    limiter_empty = TokenBucketRateLimiter(capacity=100, refill_rate=10.0)
    for _ in range(100):
        limiter_empty.check("customerC", current_time_ms=0)

    decision = limiter_empty.check("customerC", current_time_ms=0)
    assert not decision.allowed
    assert decision.remaining == 0
    assert decision.retry_after_ms == 100
    

    # 5. multiple customers maintain independent state
    decision_a = limiter.check("customerA", current_time_ms=20000)
    decision_b = limiter.check("customerB", current_time_ms=20000)
    assert decision_a.allowed
    assert decision_b.allowed
    assert decision_a.remaining == 99
    assert decision_b.remaining == 98
