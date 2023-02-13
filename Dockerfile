FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt ./

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose port 8000 for the application to listen on
EXPOSE 8000

# Specify the command to run when the container starts
CMD ["uvicorn", "ScrappingService:router", "--host", "0.0.0.0", "--port", "8000"]
