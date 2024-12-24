from .utils2 import is_loclx_installed, install_deb_package,create_config_file
import subprocess,os,time,re

def check_status():
    if is_loclx_installed():
        result = subprocess.run(["loclx", "a", "status"], capture_output=True, text=True)
        if "Error: you are not logged in, please login using your access token" in result.stdout:
            print("Please login using your access token.")
            return False
        else:
            print("Logged in.")
            return True
    else:
        install_deb_package()
        check_status()
def login(access_token):
    if not is_loclx_installed():
        install_deb_package()
        login(access_token)
    else:
        print("Logging in...")
        os.environ['ACCESS_TOKEN'] = access_token
        check_status()
def http_tunnel_start(port,access_token):
    if not check_status():
        login(access_token)
        
    print(f"Creating HTTP tunnel on port {port}...")
    subprocess.run(["sudo","loclx", "service", "stop"], check=True)
    create_config_file(port)
    subprocess.run(["loclx", "service", "uninstall"], check=True)
    subprocess.run(["loclx", "service", "install", "--config", "loclx_service_config.yaml"], check=True)
    subprocess.run(["loclx", "service", "start"], check=True)
    time.sleep(2)
    output= subprocess.run(["loclx", "tunnel", "list"], capture_output=True, text=True, check=True)
    print(output.stdout)
    # Extract the URL from the first line
    match = re.search(r'http\s+(\S+)', output.stdout)
    if match:
        url = match.group(1)
        print(f"Your service is exposed to this URL: https://{url}")
        return url
    else:
        print("No URL found.")
        return None

def http_tunnel_stop():
    print("Stopping HTTP tunnel...")
    subprocess.run(["loclx", "service", "stop"], check=True)
    subprocess.run(["loclx", "service", "uninstall"], check=True)
    print("HTTP tunnel stopped.") 

def http_tunnel_status():
    print("Checking HTTP tunnel status...")
    output= subprocess.run(["loclx", "tunnel", "list"], capture_output=True, text=True, check=True)
    print(output.stdout)
    return output.stdout



 

