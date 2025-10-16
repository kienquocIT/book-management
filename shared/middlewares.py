import time
import logging
from django.db import connection
from django.conf import settings
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from log.models import LogAction

logger = logging.getLogger(__name__)

class SQLLogToConsoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        total_time = time.time() - start

        # chỉ chạy khi DEBUG=True
        if settings.DEBUG and connection.queries:
            query_count = len(connection.queries)
            total_sql_time = sum(float(q.get("time", 0)) for q in connection.queries)

            logger.debug("=" * 80)
            logger.debug(f"📌 Path: {request.path}")
            logger.debug(f"⏱️ Request time: {round(total_time, 4)}s")
            logger.debug(f"💾 SQL queries: {query_count} in {round(total_sql_time, 4)}s")

            for i, q in enumerate(connection.queries, start=1):
                sql = q.get("sql")
                time_taken = q.get("time")
                logger.debug(f"[{i}] ({time_taken}s) {sql}")

            logger.debug("=" * 80)

        return response


class UpdateLastLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            if not request.user.last_login or (timezone.now() - request.user.last_login).seconds > 60:
                request.user.last_login = timezone.now()
                request.user.save(update_fields=["last_login"])

        return response

class LogActionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            LogAction.objects.create(
                user=request.user,
                action=f"{request.method} {request.path}",
                timestamp=timezone.now()
            )

        return response