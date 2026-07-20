import logging
import os
from urllib.parse import unquote

from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import \
    OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import \
    OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

#Trace
resource = Resource.create(
    {
        "service.name": "marginal-backend",
        "service.version": "1.0.0",
        "deployment.environment": "development",
    }
)

trace.set_tracer_provider(
    TracerProvider(resource=resource)
)

span_exporter = OTLPSpanExporter(
    endpoint=f"{os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"]}/v1/traces",
    headers = {
        "Authorization": os.environ["OTEL_EXPORTER_OTLP_HEADERS"]
            .split("=", 1)[1]
            .replace("%20", " ")
    },
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(span_exporter)
)

tracer = trace.get_tracer("marginal")


#Metrics
metric_exporter = OTLPMetricExporter(
    endpoint=f"{os.environ['OTEL_EXPORTER_OTLP_ENDPOINT']}/v1/metrics",
    headers={
        "Authorization": unquote(
            os.environ["OTEL_EXPORTER_OTLP_HEADERS"].split("=", 1)[1]
        )
    },
)

metric_reader = PeriodicExportingMetricReader(
    metric_exporter,
    export_interval_millis=5000,
)

meter_provider = MeterProvider(
    resource=resource,
    metric_readers=[metric_reader],
)

metrics.set_meter_provider(meter_provider)

meter = metrics.get_meter("marginal")

# Logging

log_exporter = OTLPLogExporter(
    endpoint=f"{os.environ['OTEL_EXPORTER_OTLP_ENDPOINT']}/v1/logs",
    headers={
        "Authorization": unquote(
            os.environ["OTEL_EXPORTER_OTLP_HEADERS"].split("=", 1)[1]
        )
    },
)

logger_provider = LoggerProvider(
    resource=resource,
)

logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(log_exporter)
)

set_logger_provider(logger_provider)


otel_handler = LoggingHandler(
    level=logging.INFO,
    logger_provider=logger_provider,
)

root_logger = logging.getLogger()

if not any(
    isinstance(handler, LoggingHandler)
    for handler in root_logger.handlers
):
    root_logger.addHandler(otel_handler)