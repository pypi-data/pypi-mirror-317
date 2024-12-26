import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time
import json
from cnb.log.log_conf import set_trace, logger
from cnb.utils.sensitive import mask_sensitive_data


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Start time for calculating duration
        uuid_data = str(uuid.uuid4()).replace("-", "")
        start_time = time.time()
        # Unique ID for this request
        request_id = uuid_data
        # Trace ID (passed from client or generated)
        trace_id = request.headers.get("X-Trace-ID", uuid_data)
        # New span ID for this request
        span_id = str(uuid.uuid4()).replace("-", "")

        set_trace(trace_id, span_id)

        # If part of an existing trace, get parent span
        parent_span_id = request.headers.get("X-Parent-Span-ID", "None")

        # Get user information and IP address
        user_id = request.headers.get("X-User-ID", "anonymous")
        transaction_id = request.headers.get("X-Transaction-ID", "N/A")
        user_ip = request.client.host

        extra_info = {
            'request_id': request_id,
            'trace_id': trace_id,
            'span_id': span_id,
            'parent_span_id': parent_span_id,
            'user_id': user_id,
            'ip_address': user_ip,
            'transaction_id': transaction_id,
            'method': request.method,
            'url': str(request.url),
            'status_code': "",
            "duration": "",
        }

        user_agent = request.headers.get("user-agent", "unknown")

        # Log incoming request
        logger.bind(request_id=request_id, user_id=user_id).info(
            f"Request received: {request.method} {request.url} | IP: {user_ip} | User-Agent: {user_agent}",
            **extra_info
        )

        # Mask headers
        headers = dict(request.headers)
        masked_headers = mask_sensitive_data(headers)
        logger.bind(request_id=request_id, user_id=user_id).info(f"Header: {masked_headers}")

        # Mask body if it's JSON
        body = await request.body()
        try:
            json_body = json.loads(body)
            masked_body = mask_sensitive_data(json_body)
            logger.bind(request_id=request_id, user_id=user_id).info(f"Body: {json.dumps(masked_body)}")
        except json.JSONDecodeError:
            logger.info(f"Body: [non-JSON or binary data omitted]")

        response = await call_next(request)

        process_time = time.time() - start_time

        # Log outgoing response
        logger.bind(request_id=request_id, user_id=user_id).info(
            f"Request processed: {request.method} {request.url} | Status: {response.status_code} | Time: {process_time:.3f}s"
        )

        return response
