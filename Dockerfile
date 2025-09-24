FROM python:3.11-slim

# Install prerequisites
RUN apt-get update && apt-get install -y \
    curl gnupg2 apt-transport-https lsb-release ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Add Microsoft repo and ODBC driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft.gpg \
    && curl https://packages.microsoft.com/config/debian/12/prod.list \
       | sed 's#deb #deb [signed-by=/usr/share/keyrings/microsoft.gpg] #' \
       > /etc/apt/sources.list.d/mssql-release.list \
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
