# Token Bucket Rate Limiter

A production-ready implementation of a **token bucket rate limiter** for API request throttling with continuous lazy refill.

## 🎯 Problem Statement

APIs need to limit customer usage to maintain service stability and fairness. This project implements a token bucket rate limiter that:
- Allows per-customer rate limits
- Refills tokens continuously based on elapsed time (not fixed intervals)
- Never lets the bucket overflow beyond capacity
- Returns accurate retry times when requests are rejected

## ✨ Key Features

- **Per-Customer Isolation**: Each customer maintains an independent token bucket
- **Continuous Refill**: Tokens refill based on elapsed time between requests, not background timers
- **Fractional Token Support**: Internal float precision handles fractional tokens seamlessly
- **Lazy Initialization**: New customers start with a full bucket and never face unjust denial
- **Accurate Retry Times**: Returns millisecond-precise wait times before retry
- **Edge Case Handling**: Supports long delays, rapid requests, and clock accuracy

## 🏗️ Architecture

### Data Structures

```python
@dataclass
class Decision:
    allowed: bool           # Is the request allowed?
    remaining: int          # Tokens left (as integer)
    retry_after_ms: int     # Milliseconds to wait if denied
```

### Design Pattern

**Lazy Refill Approach**: Instead of a background timer, tokens are refilled on-demand when a request arrives:

1. **Initialize**: New customers start with full capacity
2. **Refill**: Calculate elapsed time and add `(elapsed_ms / 1000) * refill_rate` tokens
3. **Cap**: Ensure bucket never exceeds capacity
4. **Consume**: Deduct one token if allowed
5. **Return**: Provide decision with accurate retry time

## 📊 Configuration

```python
limiter = TokenBucketRateLimiter(capacity=100, refill_rate=10.0)
```

- **capacity**: 100 tokens per bucket
- **refill_rate**: 10 tokens per second

## 🚀 Quick Start

### Run the Demo

```bash
python3 demo/simulate.py
```

Output:
```
time=0ms, customer=customer1, allowed=True, remaining=99, retry_after_ms=0
time=100ms, customer=customer1, allowed=True, remaining=99, retry_after_ms=0
time=1000ms, customer=customer1, allowed=True, remaining=99, retry_after_ms=0
...
```

### Run Tests

```bash
# First time setup
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install pytest

# Run tests
python3 -m pytest -q tests
```

Expected output: `5 passed`

## 🧪 Test Coverage

### Scenario Tests (`tests/test_scenario.py`)

- First request success and full bucket initialization
- Continuous refill over time
- Capacity enforcement (no overflow)
- Multiple customer independence
- Empty bucket denial with retry calculation

### Edge Cases (`tests/test_edge_cases.py`)

- Fractional token handling
- Rapid-fire requests at same timestamp
- Bucket depletion and recovery

### Test Results

```
5 passed in 0.01s
```

## 📁 Project Structure

```
.
├── README.md                      # This file
├── APPROACH.md                    # Problem analysis and design decisions
├── IMPLEMENTATION_NOTES.md        # Implementation details
├── AI_USAGE_LOG.md               # AI interaction log
│
├── src/
│   ├── main.py                   # Core implementation
│   └── __init__.py               # Package initialization
│
├── tests/
│   ├── test_scenario.py          # Main scenario tests
│   └── test_edge_cases.py        # Edge case tests
│
└── demo/
    └── simulate.py               # Runnable demo
```

## 🔍 Example Walkthrough

Starting with capacity=100, refill_rate=10 tokens/sec:

| Time | Requests | Refill | Result |
|------|----------|--------|--------|
| T=0ms | 60 | - | Bucket: 40 tokens |
| T=2000ms | 70 | +20 | 60 allowed, 10 denied |
| T=7000ms | 30 | +50 | All 30 allowed, Bucket: 20 |
| T=20000ms | 100 | +130 → 100 (capped) | All 100 allowed |

## 💡 Key Implementation Insights

1. **Lazy Refill**: Eliminates need for background timers; simpler and more efficient
2. **Fractional Tokens**: Storing as `float` internally provides smooth, accurate refill
3. **Ceiling Retry**: Using `ceil()` ensures clients never retry too early
4. **Customer Isolation**: Separate state per customer prevents cross-contamination

## 🛠️ Technologies

- **Language**: Python 3.14+
- **Testing**: pytest
- **Type Hints**: Full type annotations for clarity
- **Dataclasses**: Used for clean, immutable return types

## 📚 Files

- `APPROACH.md` — Detailed problem analysis and solution design
- `IMPLEMENTATION_NOTES.md` — How it works and how to run
- `AI_USAGE_LOG.md` — Full interaction history with AI assistant

## ✅ What's Working

- ✅ Per-customer token buckets
- ✅ Continuous lazy refill based on elapsed time
- ✅ Accurate retry time calculations (in milliseconds)
- ✅ Full test coverage (5 passing tests)
- ✅ Clean, production-ready code

## 🎓 Learning Outcomes

This project demonstrates:
- Rate limiting algorithms and trade-offs
- Lazy vs. eager computation
- Edge case handling in distributed systems
- Comprehensive testing practices
- Clean code principles (SOLID)

## 📝 License

MIT

---

**Built for**: Assignment AQB (Token Bucket Rate Limiter)  
**Submitted by**: U22CS026 Jay Patel  
**Date**: 2026-06-22
