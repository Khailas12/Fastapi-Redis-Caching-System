FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory to the app folder
WORKDIR /app/app

# Copy the requirements file (adjust path)
COPY requirements.txt ../

# Install dependencies
RUN pip install --no-cache-dir -r ../requirements.txt

# Copy the application code
COPY app/ .

# Run with simple main:app
CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8000"]

