FROM python:3.12-slim

WORKDIR /app

# Install pip via apt (includes setuptools and wheel)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip python3-setuptools python3-wheel \
    && rm -rf /var/lib/apt/lists/*

# Configure pip globally to use wheels directory
RUN pip3 config set global.no-index true && \
    pip3 config set global.find-links /wheels

# Copy wheels (pre-downloaded)
COPY backend/wheels/*.whl /wheels/

# Install all dependencies from local wheels
RUN pip3 install --no-cache-dir /wheels/*.whl

# Copy backend source code
COPY backend/ ./

# Expose port
EXPOSE 8000

# Run the backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
