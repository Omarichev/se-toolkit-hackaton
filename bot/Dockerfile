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
COPY bot/wheels/*.whl /wheels/

# Install all dependencies from local wheels
RUN pip3 install --no-cache-dir /wheels/*.whl

# Copy bot source code
COPY bot/ ./

# Run the bot
CMD ["python", "bot.py"]
