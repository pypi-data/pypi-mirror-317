import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from loguru import logger
import time
import json
import contextvars
from cnb.utils.sensitive import mask_sensitive_data

# Define context variables
trace_id_var = contextvars.ContextVar("trace_id", default="N/A")
span_id_var = contextvars.ContextVar("span_id", default="N/A")


def custom_formatter(record):
    trace_id = trace_id_var.get()
    span_id = span_id_var.get()
    record["extra"]["trace_id"] = trace_id
    record["extra"]["span_id"] = span_id

    return (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "trace_id={extra[trace_id]} | span_id={extra[span_id]} | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )


# Configure Loguru with the custom formatter
logger.remove()
logger.add(
    sink=lambda msg: print(msg, end="\n"),  # Output to stdout
    format=custom_formatter,
    colorize=True,
)


# Function to set trace and span IDs
def set_trace(trace_id, span_id):
    trace_id_var.set(trace_id)
    span_id_var.set(span_id)


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Start time for calculating duration
        start_time = time.time()
        # Unique ID for this request
        request_id = str(uuid.uuid4())
        # Trace ID (passed from client or generated)
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
        # New span ID for this request
        span_id = str(uuid.uuid4())
        # Set Trace ID, and Span ID
        set_trace(trace_id, span_id)

        # Get user information and IP address
        user_id = request.headers.get("X-User-ID", "anonymous")
        user_ip = request.client.host

        extra_info = {
            'request_id': request_id,
            'trace_id': trace_id,
            'span_id': span_id,
            'user_id': user_id,
            'ip_address': user_ip,
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
