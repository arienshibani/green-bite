# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add current directory files (/app) to the container
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -v --no-cache-dir -r requirements.txt

# Download required resources for NLTK
RUN python -m nltk.downloader punkt averaged_perceptron_tagger

# Run unit-tests
RUN pytest -v --maxfail=1 --disable-warnings -q

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the command to start Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
