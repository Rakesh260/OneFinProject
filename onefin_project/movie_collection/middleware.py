from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status


class RequestCounterMiddleware:
    RATE_LIMIT = 1000
    COUNTER_KEY = "request_count"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        self.ensure_cache_initialized()
        try:
            count = cache.incr(self.COUNTER_KEY)
        except ValueError:
            cache.set(self.COUNTER_KEY, 1, timeout=None)
            count = 1

        print(f"API has been called {count} times")

        if count > self.RATE_LIMIT:
            return self.rate_limit_exceeded()

        response = self.get_response(request)
        return response

    def ensure_cache_initialized(self):

        if cache.get(self.COUNTER_KEY) is None:
            cache.set(self.COUNTER_KEY, 0, timeout=None)

    def rate_limit_exceeded(self):

        response_data = {
            "error": "Too many requests",
            "message": "API rate limit exceeded, try again later."
        }
        return JsonResponse(response_data, status=status.HTTP_429_TOO_MANY_REQUESTS)
