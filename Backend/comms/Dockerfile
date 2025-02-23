# ./Portfolio-project/Backend/Dockerfile
# FROM python:3.9
FROM python:3.10-slim


WORKDIR /app

RUN pip install --upgrade pip

# Copy the requirements file
COPY requirements.txt /app/

RUN pip install --upgrade pip

# Install the dependencies
# Install system dependencies
# Install system dependencies
RUN apt-get update && apt-get install -y \
    # python3-apt \
    pkg-config \
    libgirepository1.0-dev \
    libcairo2-dev \
    cmake \
    build-essential


RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the Django project files
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
