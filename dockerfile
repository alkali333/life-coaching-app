# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container to /docker_app
WORKDIR /docker_app

# Copy requirements.txt into the container at /docker_app
COPY r .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r r

# Add the current directory contents into the container at /docker_app
COPY ./app .

# Expose port 8501 (default Streamlit port)
EXPOSE 8501

# Run Streamlit app
CMD streamlit run main.py
