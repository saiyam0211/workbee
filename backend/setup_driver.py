import os
import time
import subprocess
print("Running script...")
result = subprocess.run(['bash', 'script.sh'], capture_output=True, text=True)

time.sleep(4)

