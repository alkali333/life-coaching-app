# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container to /docker_app
WORKDIR /docker_app

# Install ffmpeg (and other dependencies) first
RUN apt-get update && apt-get install -y ffmpeg

# Copy requirements.txt into the container at /docker_app
COPY r .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r r

# Add the current directory contents into the container at /docker_app
COPY ./app .


EXPOSE 8080

# Run Streamlit app
CMD streamlit run main.py --server.port 8080
