## AI Interaction #1
Time: 2026-06-22 16:57:45 IST
Tool: assistant
My Prompt: problem: I am solving a Token Bucket Rate Limiter assignment... now just give me the best design approach, data structure no code needed for now
What I Kept: the assignment requirements and the need for a clean design focused on lazy refill, per-customer state, and exact retry timing.
What I Changed/Rejected: Provided a high-level architecture with customer state, refill formula, and decision flow. I intentionally avoided code and focused on the correct logical design.

## AI Interaction #2
Time: 2026-06-22 16:58:12 IST
Tool: assistant
My Prompt: now create only data structures and class definitions for the problem in python: requirements: decision dataclass, tokenBucketRateLimiter, appropriate instance variables do not implement any methods
What I Kept: the need for a Python skeleton with only the requested data structures and instance variables.
What I Changed/Rejected: Created `src/types.py` containing a `Decision` dataclass and a `TokenBucketRateLimiter` class with `capacity`, `refill_rate`, `buckets`, and `last_refill` instance variables. I did not implement any methods yet.

## AI Interaction #3
Time: 2026-06-22 16:58:34 IST
Tool: assistant
My Prompt: now I need Customer Initialization... return only relevant methods and time in ms; add refill logic...
What I Kept: the requirement to initialize new customers with full capacity and store the timestamp in milliseconds.
What I Changed/Rejected: Added `initialize_customer` and `refill_bucket` to `src/types.py`, including lazy refill logic with fractional tokens and capacity capping. I did not add unrelated methods.

## AI Interaction #4
Time: 2026-06-22 16:58:55 IST
Tool: assistant
My Prompt: yes now implement request handling check(customer_id, current_timr_ms) method... do not implement test yet
What I Kept: the full request handling flow with initialization, refill, token consumption, and Decision return.
What I Changed/Rejected: Implemented `check` in `src/types.py`, ensuring the bucket is initialized for new customers, refilled before evaluation, decremented on success, and a `Decision` object returned.

## AI Interaction #5
Time: 2026-06-22 16:59:15 IST
Tool: assistant
My Prompt: now implement retry calculations - until bucket reaches at least one token - return miliseconds
What I Kept: the requirement that denied requests return a millisecond delay until at least one token is available.
What I Changed/Rejected: Updated the retry logic to compute the exact wait time using `ceil((tokens_needed / refill_rate) * 1000)` and return that as `retry_after_ms`.

## AI Interaction #6
Time: 2026-06-22 16:59:40 IST
Tool: assistant
My Prompt: now convert all this in pased image format i.e main.py -no need of utils -create dirctory for test and with the casess -create demo that can run all these
What I Kept: the request to organize the implementation into a clean repo structure with `main.py`, tests, and demo.
What I Changed/Rejected: Created `src/main.py`, `tests/test_scenario.py`, `tests/test_edge_cases.py`, and `demo/simulate.py`. I skipped adding a separate `utils` folder as requested.

## AI Interaction #7
Time: 2026-06-22 17:00:10 IST
Tool: assistant
My Prompt: now create one test for the problem 1. first request succeeds 2. buckets starts with full capacity 3. continuous refill 4. capacity = 100 works 5. retry time calculations 6. multiple customers 7. empty bucket behavior
What I Kept: the comprehensive list of test requirements for the token bucket implementation.
What I Changed/Rejected: Added a single comprehensive test in `tests/test_scenario.py` that covers initialization, refill, capacity, retry values, and multiple-customer independence.

## AI Interaction #8
Time: 2026-06-22 17:02:00 IST
Tool: assistant
My Prompt: now test the code with this specs capacity =100 refill rate = 10 tokens/sec T=0 60 requests T=2000 ms 70 re T= 7000 ms 30 re T= 20000 ms 100 re show bucket state after eery steps
What I Kept: the exact scenario details and bucket-state expectations.
What I Changed/Rejected: Ran the simulation in the workspace and reported the bucket state and outcomes for each time step. I kept the scenario faithful to your specification.

## AI Interaction #9
Time: 2026-06-22 17:03:12 IST
Tool: assistant
My Prompt: yes and now finally check demo.py works perfectly or not
What I Kept: the request to verify `demo/simulate.py` execution.
What I Changed/Rejected: Fixed the import issue by adding `src/__init__.py` and module path adjustment in `demo/simulate.py`, then confirmed the demo runs successfully.

## AI Interaction #10
Time: 2026-06-22 17:05:45 IST
Tool: assistant
My Prompt: - `python3 -m pip install pytest`
What I Kept: the explicit installation request for pytest.
What I Changed/Rejected: Installed pytest in the workspace environment using the available package installation tool.

## AI Interaction #11
Time: 2026-06-22 17:06:10 IST
Tool: assistant
My Prompt: - `python3 -m pytest -q tests`
What I Kept: the request to run the full test suite.
What I Changed/Rejected: Diagnosed the interpreter mismatch, created a local virtual environment, and verified pytest execution in that environment.

## AI Interaction #12
Time: 2026-06-22 17:11:30 IST
Tool: assistant
My Prompt: write readme for me
What I Kept: the need for a recruiter-facing README that explains the project clearly.
What I Changed/Rejected: Created `README.md` with project overview, quick start instructions, architecture, tests, and validation results.

## AI Interaction #13
Time: 2026-06-22 17:12:20 IST
Tool: assistant
My Prompt: yes add
What I Kept: the need to include usage instructions in `IMPLEMENTATION_NOTES.md`.
What I Changed/Rejected: Added a `How to run` section to `IMPLEMENTATION_NOTES.md` describing demo and test execution.


