# Step 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy the requirements file into the container
COPY req.txt /app/

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r req.txt

# Step 5: Copy the rest of the application code
COPY . /app/

# Step 6: Set environment variables for Django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 7: Expose the port the app runs on
EXPOSE 8000

# Step 8: Run migrations and start the server
CMD ["python", "manage.py", "migrate", "test"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
