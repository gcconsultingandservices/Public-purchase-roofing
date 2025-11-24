# Use Python 3.13 slim image
FROM python:3.13-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg2 \
    unzip \
    xvfb \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk1.0-0 \
    libcups2 \
    libgtk-3-0 \
    libgbm1 \
    libpangocairo-1.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxrender1 \
    libx11-xcb1 \
    ca-certificates \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Add Google Chrome signing key and repo
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux-signing-key.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set display port (required for headless Chrome)
ENV DISPLAY=:99

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run the Python script
CMD ["python", "Main.py"]
