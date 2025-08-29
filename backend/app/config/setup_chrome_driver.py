import os
import subprocess
import urllib.request
import zipfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def find_chrome_binary():
    """Find Chrome binary in various possible locations"""
    possible_paths = [
        '/usr/bin/google-chrome',
        '/usr/bin/google-chrome-stable',
        '/usr/bin/chromium-browser',
        '/usr/bin/chromium',
        '/opt/google/chrome/chrome',
        '/opt/render/project/.render/chrome/opt/google/chrome/chrome'  # Render custom path
    ]
    
    for path in possible_paths:
        if os.path.exists(path) and os.path.isfile(path):
            print(f"Found Chrome binary at: {path}")
            return path
    
    # Try to find Chrome using which command
    for chrome_name in ['google-chrome', 'google-chrome-stable', 'chromium']:
        try:
            result = subprocess.run(['which', chrome_name], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                chrome_path = result.stdout.strip()
                print(f"Found Chrome binary via 'which': {chrome_path}")
                return chrome_path
        except:
            continue
    
    return None

def get_chrome_version(chrome_path):
    """Get Chrome version from binary"""
    try:
        result = subprocess.run([chrome_path, '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_output = result.stdout.strip()
            version_parts = version_output.split()
            for part in version_parts:
                if '.' in part and part.replace('.', '').replace('-', '').isdigit():
                    return part
        return None
    except Exception as e:
        print(f"Error getting Chrome version: {e}")
        return None

def download_compatible_chromedriver():
    """Download ChromeDriver compatible with the installed Chrome version"""
    try:
        chrome_path = find_chrome_binary()
        if not chrome_path:
            print("Chrome binary not found.")
            return None
        
        chrome_version = get_chrome_version(chrome_path)
        if not chrome_version:
            print("Could not determine Chrome version")
            return None
        
        chrome_major = chrome_version.split('.')[0]
        print(f"Chrome version: {chrome_version}, Major: {chrome_major}")
        
        # Set ChromeDriver directory
        if os.path.exists('/opt/render/project/.render'):
            chromedriver_dir = '/opt/render/project/.render/chromedriver'
        else:
            chromedriver_dir = '/app/.render/chromedriver'
        
        os.makedirs(chromedriver_dir, exist_ok=True)
        chromedriver_path = os.path.join(chromedriver_dir, 'chromedriver')
        
        # Clean up old installations
        if os.path.exists(chromedriver_path):
            os.remove(chromedriver_path)
        
        # Download ChromeDriver
        if int(chrome_major) >= 115:
            base_url = "https://storage.googleapis.com/chrome-for-testing-public"
            download_url = f"{base_url}/{chrome_version}/linux64/chromedriver-linux64.zip"
            
            try:
                print(f"Downloading ChromeDriver for version {chrome_version}")
                urllib.request.urlretrieve(download_url, os.path.join(chromedriver_dir, 'chromedriver.zip'))
            except Exception as e:
                print(f"Exact version failed, trying fallbacks: {e}")
                fallback_versions = ["131.0.6778.85", "130.0.6723.91", "129.0.6668.89", "128.0.6613.84"]
                downloaded = False
                
                for fallback in fallback_versions:
                    try:
                        download_url = f"{base_url}/{fallback}/linux64/chromedriver-linux64.zip"
                        urllib.request.urlretrieve(download_url, os.path.join(chromedriver_dir, 'chromedriver.zip'))
                        print(f"Downloaded fallback version: {fallback}")
                        downloaded = True
                        break
                    except:
                        continue
                
                if not downloaded:
                    return None
        else:
            # Legacy API for older Chrome versions
            try:
                version_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{chrome_major}"
                response = urllib.request.urlopen(version_url)
                chromedriver_version = response.read().decode().strip()
                download_url = f"https://chromedriver.storage.googleapis.com/{chromedriver_version}/chromedriver_linux64.zip"
                urllib.request.urlretrieve(download_url, os.path.join(chromedriver_dir, 'chromedriver.zip'))
            except Exception as e:
                print(f"Legacy API failed: {e}")
                return None
        
        # Extract ChromeDriver
        zip_path = os.path.join(chromedriver_dir, 'chromedriver.zip')
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(chromedriver_dir)
        
        # Handle different archive structures
        if os.path.exists(os.path.join(chromedriver_dir, 'chromedriver-linux64', 'chromedriver')):
            shutil.move(
                os.path.join(chromedriver_dir, 'chromedriver-linux64', 'chromedriver'),
                chromedriver_path
            )
            shutil.rmtree(os.path.join(chromedriver_dir, 'chromedriver-linux64'))
        
        # Clean up
        os.remove(zip_path)
        
        # Set permissions
        os.chmod(chromedriver_path, 0o755)
        
        if os.path.exists(chromedriver_path):
            print(f"ChromeDriver installed at: {chromedriver_path}")
            return chromedriver_path
        
        return None
        
    except Exception as e:
        print(f"Error downloading ChromeDriver: {e}")
        return None

def get_chrome_options():
    """Get Chrome options optimized for serverless/container environments"""
    chrome_options = Options()
    
    # Essential options for headless operation
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-plugins')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-background-timer-throttling')
    chrome_options.add_argument('--disable-backgrounding-occluded-windows')
    chrome_options.add_argument('--disable-renderer-backgrounding')
    chrome_options.add_argument('--disable-features=TranslateUI')
    chrome_options.add_argument('--disable-ipc-flooding-protection')
    chrome_options.add_argument('--memory-pressure-off')
    chrome_options.add_argument('--max_old_space_size=4096')
    
    # Set Chrome binary if found
    chrome_path = find_chrome_binary()
    if chrome_path:
        chrome_options.binary_location = chrome_path
        print(f"Using Chrome binary: {chrome_path}")
    
    return chrome_options

def setup_chrome():
    """Setup Chrome and ChromeDriver"""
    try:
        print("Setting up Chrome environment...")
        
        chrome_path = find_chrome_binary()
        if not chrome_path:
            print("Chrome not found!")
            return False
            
        chromedriver_path = download_compatible_chromedriver()
        if not chromedriver_path:
            print("Failed to setup ChromeDriver")
            return False
            
        # Store paths for later use
        os.environ['CHROME_BINARY_PATH'] = chrome_path
        os.environ['CHROMEDRIVER_PATH'] = chromedriver_path
        
        # Test the setup
        print("Testing Chrome setup...")
        driver = get_webdriver()
        if driver:
            driver.get("https://www.google.com")
            print(f"Test successful! Page title: {driver.title}")
            driver.quit()
            return True
        else:
            print("WebDriver test failed")
            return False
            
    except Exception as e:
        print(f"Chrome setup failed: {e}")
        return False

def get_webdriver():
    """Get configured WebDriver instance"""
    try:
        chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')
        if not chromedriver_path or not os.path.exists(chromedriver_path):
            if not setup_chrome():
                return None
            chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')
        
        chrome_options = get_chrome_options()
        service = Service(executable_path=chromedriver_path)
        
        return webdriver.Chrome(service=service, options=chrome_options)
        
    except Exception as e:
        print(f"Error creating WebDriver: {e}")
        return None