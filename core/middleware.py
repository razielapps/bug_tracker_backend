import logging

logger = logging.getLogger(__name__)

class IPLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        path = request.path
        method = request.method

        logger.info(f"[{method}] Request from {ip} to {path}")

        response = self.get_response(request)
        return response
