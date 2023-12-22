# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the working directory
COPY . /app

# Install the application dependencies
RUN pip install -r requirements.txt

# Define the entry point for the container
ENTRYPOINT ["python", "--host=0.0.0.0:8080"]

# configure the container to run in an executed manner
CMD ["app.py" ]

EXPOSE 8080