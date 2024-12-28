import contextvars
import logging

from loguru import logger

# Disable Uvicorn logs
# Suppress all Uvicorn logs
logging.getLogger("uvicorn").disabled = True
logging.getLogger("uvicorn.error").disabled = True
logging.getLogger("uvicorn.access").disabled = True

# Define context variables
trace_id_var = contextvars.ContextVar("trace_id", default="N/A")
span_id_var = contextvars.ContextVar("span_id", default="N/A")


def custom_formatter(record):
    trace_id = trace_id_var.get()
    span_id = span_id_var.get()
    record["extra"]["trace_id"] = trace_id
    record["extra"]["span_id"] = span_id
    return (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
        "<level>{level}</level> "
        "{extra[trace_id]}-{extra[span_id]} "
        "<cyan>{name}.{function}</cyan> - <level>{message}</level>"
    )


# Configure Loguru with the custom formatter
logger.remove()
logger.add(
    sink=lambda msg: print(msg, end="\n"),  # Output to stdout
    format=custom_formatter,
    backtrace=True,
    diagnose=True
)


# Function to set trace and span IDs
def set_trace(trace_id, span_id):
    trace_id_var.set(trace_id)
    span_id_var.set(span_id)
