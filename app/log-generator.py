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
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)


def setup_logger(name: str) -> logging.Logger:
    """Setup structured JSON logger"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Remove default handlers
    logger.handlers = []
    
    # Add stdout handler with JSON formatter
    handler = logging.StreamHandler()
    formatter = JSONFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


def generate_sample_messages() -> list:
    """Generate sample log messages for demo"""
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


def main():
    """Main log generator loop"""
    logger = setup_logger("logpulse")
    messages = generate_sample_messages()
    log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
    
    service_name = os.getenv("SERVICE_NAME", "log-generator")
    interval = float(os.getenv("LOG_INTERVAL", "2"))
    
    print(f"🚀 Starting Log Generator", flush=True)
    print(f"   Service: {service_name}", flush=True)
    print(f"   Interval: {interval}s", flush=True)
    print(f"   Target: Loki via Promtail", flush=True)
    print("=" * 60, flush=True)
    
    counter = 0
    
    try:
        while True:
            counter += 1
            
            # Pick random log level and message
            level = random.choice(log_levels)
            message = random.choice(messages)
            
            # Add context
            request_id = f"req-{counter:06d}"
            user_id = f"user-{random.randint(1, 100):03d}"
            enhanced_message = f"[{request_id}] [{user_id}] {message}"
            
            # Log with appropriate level
            log_func = getattr(logger, level.lower())
            log_func(enhanced_message)
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n⏹️  Log Generator stopped", flush=True)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
