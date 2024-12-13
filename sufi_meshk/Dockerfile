# Base image
FROM python:3.10-slim

# Install Doppler CLI
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg && \
    curl -sLf --retry 3 --tlsv1.2 --proto "=https" 'https://packages.doppler.com/public/cli/gpg.DE2A7741A397C129.key' | \
    gpg --dearmor -o /usr/share/keyrings/doppler-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/doppler-archive-keyring.gpg] https://packages.doppler.com/public/cli/deb/debian any-version main" | \
    tee /etc/apt/sources.list.d/doppler-cli.list && \
    apt-get update && \
    apt-get -y install doppler && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files to the container
COPY . /app/

# Adjust ownership and permissions for static and media files
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R www-data:www-data /app/staticfiles /app/media && \
    chmod -R 755 /app/staticfiles /app/media

# Inject environment variables using Doppler at runtime
CMD ["doppler", "run", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
