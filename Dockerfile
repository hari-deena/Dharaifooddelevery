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

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
