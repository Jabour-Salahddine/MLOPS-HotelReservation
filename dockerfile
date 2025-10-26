# Use a lightweight Python image
FROM python:3.10-slim

# Prevent Python from writing .pyc files & ensure output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# ---- Install system dependencies ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    gcc \
    g++ \
    libgomp1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# ---- Install Python dependencies ----
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -e .

# ---- Train the model before running the app ----
RUN python pipline/training_pipline.py

# Expose Flask port
EXPOSE 5000

# ---- Run the app ----
CMD ["python", "app.py"]
