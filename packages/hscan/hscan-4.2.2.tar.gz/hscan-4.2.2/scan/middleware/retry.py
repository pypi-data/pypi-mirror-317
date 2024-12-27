from tenacity import retry, stop_after_attempt, wait_exponential

class RetryMiddleware:
    def __init__(self, max_attempts=3, wait_min=1, wait_max=10):
        self.max_attempts = max_attempts
        self.wait_min = wait_min
        self.wait_max = wait_max
        
    @retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=wait_min, max=wait_max)
    )
    async def execute(self, func, *args, **kwargs):
        return await func(*args, **kwargs) 