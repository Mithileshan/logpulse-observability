#!/usr/bin/env python3
"""
Log Generator - Produces structured JSON logs for observability testing
"""

import json
import time
import random
import logging
import os
from datetime import datetime
from typing import Dict, Any

# Configure structured logging to stdout
class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "service": os.getenv("SERVICE_NAME", "log-generator"),
            "message": record.getMessage(),
            "logger": record.name,
        }

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def setup_logger(name: str) -> logging.Logger:
    """Setup structured JSON logger"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.handlers = []
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    return logger


def normal_messages() -> list:
    return [
        "User login successful",
        "Database query executed",
        "Cache hit for key",
        "API request processed",
        "Worker task completed",
        "Scheduled job triggered",
        "Configuration reloaded",
        "Health check passed",
        "Metrics collected",
        "Service initialized",
        "Request validated",
        "Response sent to client",
        "Event processed",
        "Transaction committed",
        "Session created",
    ]


def failure_messages() -> list:
    return [
        "Database connection timeout after 30s",
        "Failed to acquire lock on resource",
        "Upstream service returned 503",
        "Memory threshold exceeded: 92% used",
        "Request queue backed up: 847 pending",
        "Circuit breaker OPEN for payments-service",
        "Retry limit reached for job processor",
        "Disk I/O error on /var/data volume",
        "Authentication token validation failed",
        "Null pointer exception in order handler",
        "Connection pool exhausted: 0/50 available",
        "Cache eviction rate critical: 98%",
        "Health check FAILED for downstream API",
        "Deadlock detected in transaction batch",
        "Rate limit exceeded: 429 from external API",
    ]


def main():
    logger = setup_logger("logpulse")
    service_name = os.getenv("SERVICE_NAME", "log-generator")
    interval = float(os.getenv("LOG_INTERVAL", "2"))
    failure_mode = os.getenv("FAILURE_MODE", "false").lower() == "true"

    mode_label = "FAILURE MODE" if failure_mode else "normal"
    print(f"Starting Log Generator", flush=True)
    print(f"   Service: {service_name}", flush=True)
    print(f"   Mode: {mode_label}", flush=True)
    print(f"   Interval: {0.5 if failure_mode else interval}s", flush=True)
    print(f"   Target: Loki via Promtail", flush=True)
    print("=" * 60, flush=True)

    counter = 0

    try:
        while True:
            counter += 1
            request_id = f"req-{counter:06d}"
            user_id = f"user-{random.randint(1, 100):03d}"

            if failure_mode:
                # 80% ERROR, 15% WARNING, 5% INFO — fires alert within ~1 minute
                level = random.choices(
                    ["ERROR", "WARNING", "INFO"],
                    weights=[80, 15, 5]
                )[0]
                message = random.choice(failure_messages())
                sleep_interval = 0.5
            else:
                level = random.choice(["INFO", "WARNING", "ERROR", "DEBUG"])
                message = random.choice(normal_messages())
                sleep_interval = interval

            enhanced_message = f"[{request_id}] [{user_id}] {message}"
            log_func = getattr(logger, level.lower())
            log_func(enhanced_message)

            time.sleep(sleep_interval)

    except KeyboardInterrupt:
        print("\nLog Generator stopped", flush=True)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
