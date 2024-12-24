import os
import requests
import subprocess
import yaml

download_url = "https://api.localxpose.io/api/downloads/loclx-linux-amd64.deb"
local_file = "loclx-linux-amd64.deb"

def is_loclx_installed():
    try:
        # Check if loclx is installed by running 'loclx --version'
        result = subprocess.run(['loclx', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def is_file_downloaded(local_filename):
    return os.path.isfile(local_filename)

def download_file(url, local_filename):
    if is_file_downloaded(local_filename):
        print(f"{local_filename} already exists. Skipping download.")
        return local_filename
    
    # Send a GET request to the URL
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        # Open a local file with write-binary mode
        with open(local_filename, 'wb') as f:
            # Write the content to the local file in chunks
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def install_deb_package(local_filename="loclx-linux-amd64.deb", download_url="https://api.localxpose.io/api/downloads/loclx-linux-amd64.deb"):
    if is_loclx_installed():
        print("loclx is already installed. Skipping installation.")
        return
    if not is_file_downloaded(local_filename):
        print(f"{local_filename} does not exist. Downloading now...")
        download_file(download_url, local_filename)
    
    print(f"Installing {local_filename}...")
    subprocess.run(["sudo", "dpkg", "-i", local_filename], check=True)

def create_config_file(port):
    filename = 'loclx_service_config.yaml'

    # Check if file exists and delete it
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Deleted existing {filename}")

    # Define the configuration structure
    config = {
        'http_service': {
            'type': 'http',
            'region': 'us',
            'to': f'localhost:{port}'
        }
    }

    # Write to YAML file
    with open(filename, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
    print(f"Created new {filename}")


