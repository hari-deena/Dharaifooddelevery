# # Use the official Python image
# FROM python:3.12-slim

# # Set working directory
# WORKDIR /app

# # Copy dependencies file
# COPY requirements.txt .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy entire project to container
# COPY . .

# # Expose the port FastAPI runs on
# EXPOSE 8000

# # Command to start the FastAPI app
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Upgrade pip first
RUN pip install --upgrade pip --no-cache-dir

# Then install all dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy app code
COPY . .

# Expose port (if using FastAPI)
EXPOSE 8000

# Command to run
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
