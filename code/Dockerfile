# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and application code
COPY requirements.txt .
COPY app.py .
COPY iris_model.pkl .

# Copy the templates and static folders
COPY templates/ ./templates/
COPY static/ ./static/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
