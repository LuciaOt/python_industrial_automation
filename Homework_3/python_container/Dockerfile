# Use official Python slim image
FROM python:3.12.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY transform_data.py .
COPY datasets/ datasets/

# Set environment variable for Python to not buffer output (logs show immediately)
ENV PYTHONUNBUFFERED=1

# Default command to run the transformer script
CMD ["python", "transform_data.py"]
