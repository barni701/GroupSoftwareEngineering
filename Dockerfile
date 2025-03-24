# Use an official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy project files
COPY djangoProject /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files (optional)
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

# Start server
CMD ["gunicorn", "djangoProject.wsgi:application", "--bind", "0.0.0.0:8000"]