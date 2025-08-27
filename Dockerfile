# Use lightweight Python
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements2.txt .
RUN pip install --no-cache-dir -r requirements2.txt

# Copy app code
COPY . .

# Expose Flask port
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]
