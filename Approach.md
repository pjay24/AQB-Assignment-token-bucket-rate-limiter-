
ASSIGNMENT (AQB)
Submitted by:U22CS026 Jay Patel

**Problem Understanding**

The goal is to implement a Token bucket rate limiter for API customers. 
(Limits the usage).

- each customer has own bucket with:
    max_capacity= 100 tokens
    Refill rate= 10 tokens per second
    each request consumes 1 token

- System requirements:
    1. request should be processed even if 1 token is available.
    2. reject if no tokns left.
    3. use retry time for rejected requests.
    4. refill tokens based on elapsed time.
    5. bucket should not be overflowed.
    6. each customer need their separate state.

- we need to solve two main problems
    1. some customers were denied on their first request.
    2. retry after ms was returned incorrectly.

**Assumptions**

1. Each customer has independent bucket.
2. A new customer is started with a full bucket (problem 1 in 1st section).
3. current_time_ms values are monotonic.
4. The rate limiter is called only when requests arrive.
5. capacity and refill rate should be constant during runtime

**Errors**

1. we have retry_after_ms in interface (Contradiction)

retry_after_ms: int // milliseconds to wait before retrying (0 if allowed)

it shows millisecons to wait

When a request is denied, retry_after_ms must equal the number of seconds the client needs to wait until the
bucket will have at least 1 token. (Note: the field name says "ms" — pay careful attention to the unit.)

but this contradicts the interface.

so the field name is retry_after_ms so I will return the millisectons 
(convert seconds to the milliseconds if required)

2. In problem 3 we have that
- Refill tokens continuously based on elapsed time since the last request — not on a fixed interval.
but suggested solustion shows 
-  Implement a background timer that fires every 1 second and adds refill_rate tokens to
each active customer's bucket.

both are different in real use:

I will implement lazy refill during request processing based on elapsed time.

3. Batch vs 1 request
- example says multiple requests arrives but API is designed for single request

example should be treated as multiple runtimes.

4. tokens in whole number vs fractions
- examples shows only whole numbers but the program may produce tokens like 51.2
- I stores as floating point values but present remaining should be whole integer as <1 token cannot be served.

**Bugs**

1. line 21 self.buckets[customer_id] = 0 # BUG: should start at capacity

this is the problem why first request is denied 

solution: self.buckets[customer_id] = self.capacity

2. 28 # BUG: missing cap at capacity

26 self.buckets[customer_id] += tokens_to_add
27 self.last_refill[customer_id] = current_time_ms

we need to use minimum of self capacity and tokens to add

3. 43 retry_after_ms=int(retry_after_seconds) # BUG: value is seconds, not ms

solution : retry_after_ms=int(retry_after_seconds * 1000)

**My Solution**

- Two dictionaries 
    1. buckets[customer_id]
    2. last_refill[customer_id]

- Flow
    1. Load customer state
    2. Calculate elapsed time
    3. calculate refill amount
    4. apply refill and cap
    5. check availability
    6. compute retry time

tradeoff: refill is computed only when requests arrive.

**Limitations**

- floating point precision errors
- no bucket cleanup for inactive users
- no clock rollback 

**Walkthrough**

1. T=0 

Bucket=100
request = 100
remain = 40

2. T = 2000ms
(2 sec elapsed)
refill 20 tokens 
bucket= 60
request =70
only 60 allowed

3. T= 7000ms
(5 sec elapsed)
refill 50
bucket = 50
request =30
remain = 20

(we need to cap the bucket at 100, no more refills allowed after this)
