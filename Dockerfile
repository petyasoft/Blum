FROM python:3.11-alpine3.20 as builder

# Set the working directory
WORKDIR /build

# Install system dependencies required for building Python packages
RUN apk add --no-cache \
    build-base \
    python3-dev \
    libpq-dev \
    gcc

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt

# Runner stage
FROM python:3.11-alpine3.20 as runner

# Set the working directory
WORKDIR /app

# Copy only the installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .

# Command to run the application
CMD ["python3", "main.py", "-a", "1"]
