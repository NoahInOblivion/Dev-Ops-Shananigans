from prometheus_client import Counter, Histogram


REQUEST_COUNT = Counter("http_requests_total", "HTTP request count", ["method", "path", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["method", "path"])
