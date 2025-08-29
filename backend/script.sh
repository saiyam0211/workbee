#!/usr/bin/env bash
# Improved build script with better Chrome/ChromeDriver setup
set -o errexit

echo "Starting build process..."

# Install system dependencies
echo "Installing system dependencies..."
apt-get update
apt-get install -y wget unzip curl python3 python3-pip

# Use Render's persistent storage directory
STORAGE_DIR=/opt/render/project/.render
mkdir -p $STORAGE_DIR

# Install Google Chrome
if [[ ! -f "$STORAGE_DIR/chrome/opt/google/chrome/chrome" ]]; then
  echo "Installing Google Chrome..."
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  
  # Download and install Chrome
  wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm google-chrome-stable_current_amd64.deb
  
  # Make Chrome executable
  chmod +x $STORAGE_DIR/chrome/opt/google/chrome/chrome
  
  echo "Chrome installed successfully at: $STORAGE_DIR/chrome/opt/google/chrome/chrome"
else
  echo "Using Chrome from cache"
fi

# Verify Chrome installation
CHROME_PATH="$STORAGE_DIR/chrome/opt/google/chrome/chrome"
if [[ -f "$CHROME_PATH" ]]; then
  echo "Chrome binary found at: $CHROME_PATH"
  # Test Chrome version
  $CHROME_PATH --version || echo "Warning: Could not get Chrome version"
else
  echo "Error: Chrome binary not found at expected location"
  exit 1
fi

# Create a dedicated ChromeDriver directory
CHROMEDRIVER_DIR="$STORAGE_DIR/chromedriver"
mkdir -p $CHROMEDRIVER_DIR

echo "ChromeDriver will be downloaded by Python script at runtime"
echo "Chrome setup completed successfully"

# Install Python dependencies
echo "Installing Python dependencies..."
cd /opt/render/project/src
if command -v uv &> /dev/null; then
    echo "Using uv to install dependencies..."
    uv sync
else
    echo "Using pip to install dependencies..."
    pip install -r requirements.txt
fi

# Create environment file with Chrome path
echo "Creating environment variables file..."
echo "CHROME_BINARY_PATH=$CHROME_PATH" > $STORAGE_DIR/env_vars
echo "CHROMEDRIVER_DIR=$CHROMEDRIVER_DIR" >> $STORAGE_DIR/env_vars

# Make the environment variables available
export CHROME_BINARY_PATH="$CHROME_PATH"
export CHROMEDRIVER_DIR="$CHROMEDRIVER_DIR"

echo "Build completed successfully!"
echo "Chrome binary: $CHROME_BINARY_PATH"
echo "ChromeDriver directory: $CHROMEDRIVER_DIR"