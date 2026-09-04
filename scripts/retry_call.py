#!/usr/bin/env python3
"""Retry wrapper for model calls with exponential backoff.
Used by run_picks.py to handle transient provider timeouts.
"""
import time
import random

def retry_call(fn, max_attempts=3, base_delay=2.0, max_delay=30.0):
    """
    Call fn() with exponential backoff + jitter.
    Returns (status, response) from the last attempt.
    """
    delay = base_delay
    for attempt in range(1, max_attempts + 1):
        status, resp = fn()
        if status == 200:
            return status, resp
        if attempt == max_attempts:
            return status, resp
        sleep = min(delay * (2 ** (attempt - 1)), max_delay)
        sleep += random.uniform(0, 1)  # jitter
        time.sleep(sleep)
    return status, resp
