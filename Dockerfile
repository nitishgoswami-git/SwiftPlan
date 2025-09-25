FROM python:3.11-slim

# Install prerequisites
RUN apt-get update && apt-get install -y \
    curl gnupg2 apt-transport-https lsb-release ca-certificates \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Add Microsoft repo and ODBC driver (using Ubuntu 22.04 repo for better compatibility)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Flask environment
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0

# Use Gunicorn for production and bind to Render's assigned port
CMD ["sh", "-c", "gunicorn run:app --bind 0.0.0.0:${PORT}"]
