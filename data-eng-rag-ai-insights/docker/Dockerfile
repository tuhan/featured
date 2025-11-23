# Lightweight Python image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Set environment
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy your app
COPY . .

# Expose Flask port
EXPOSE 8080

# Run your server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "msin0166-individual-docker:app"]