# Uses Python 3.12.10 on Alpine 3.21 (latest GA as of 22 May 2025)
FROM python:3.12.10-alpine3.21

# Set the working directory in the container
WORKDIR /app

# system dependencies for the Python driver
RUN apk add --no-cache mariadb-connector-c-dev build-base

# Install system dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY app.py .

# Expose the port the app runs on
EXPOSE 8000

# Start the application
CMD ["python", "app.py"]
