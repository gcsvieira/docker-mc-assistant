# Use Python 3.13 to maintain audioop-lts compatibility
FROM python:3.13-slim

WORKDIR /app

# Install our dependencies directly
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt audioop-lts

# Copy our codebase from the src directory
# This keeps the image lean by excluding knowledge-base, docs, etc. (see .dockerignore)
COPY src/ .

# Run the bot
CMD ["python", "bot.py"]
