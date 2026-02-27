FROM python:3.11-slim

WORKDIR /app

# Copy the log generator script
COPY log-generator.py .

# Make it executable
RUN chmod +x log-generator.py

# Run the log generator
CMD ["python", "log-generator.py"]
