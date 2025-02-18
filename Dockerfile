# Use an official Python base image
FROM python:3.12.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local code to the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Run the script
CMD ["python", "main.py"]