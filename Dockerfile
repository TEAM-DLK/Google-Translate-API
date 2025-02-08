# Use the official Python image as the base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot script and other necessary files
COPY . .

# Expose the port (if needed for webhook-based bots)
EXPOSE 8443

# Command to run the bot
CMD ["python", "main.py"]
