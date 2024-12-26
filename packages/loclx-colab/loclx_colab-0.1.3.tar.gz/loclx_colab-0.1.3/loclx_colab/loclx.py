from .utils2 import is_loclx_installed, install_deb_package, create_config_file
import subprocess
import os
import time
import re
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TunnelError(Exception):
    """Custom exception for tunnel-related errors"""
    pass

def check_status() -> bool:
    """Check login status of loclx"""
    try:
        if is_loclx_installed():
            result = subprocess.run(["loclx", "a", "status"], 
                                  capture_output=True, 
                                  text=True,
                                  check=True)
            if "Error: your access token is invalid" in result.stdout:
                logger.warning("Not logged in. Logging in...")
                return False
            logger.info("Successfully logged in.")
            return True
        else:
            logger.info("loclx not installed. Installing...")
            install_deb_package()
            return check_status()
    except subprocess.CalledProcessError as e:
        logger.error(f"Error checking status: {str(e)}")
        raise TunnelError(f"Failed to check status: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in check_status: {str(e)}")
        raise

def login(access_token: str) -> None:
    """Login to loclx with access token"""
    if not access_token:
        raise ValueError("Access token cannot be empty")

    try:
        if not is_loclx_installed():
            logger.info("loclx not installed. Installing...")
            install_deb_package()
            login(access_token)
        else:
            logger.info("Logging in...")
            os.environ['ACCESS_TOKEN'] = access_token
            if not check_status():
                raise TunnelError("Failed to login with provided access token")
    except TunnelError:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise TunnelError(f"Login failed: {str(e)}")

def http_tunnel_start(port: int, access_token: str) -> Optional[str]:
    """Start HTTP tunnel on specified port"""
    if not isinstance(port, int) or port < 1 or port > 65535:
        raise ValueError("Invalid port number")

    try:
        if not check_status():
            login(access_token)

        logger.info(f"Creating HTTP tunnel on port {port}...")

        # Stop existing service
        subprocess.run(["sudo", "loclx", "service", "stop"], 
                      check=True, 
                      capture_output=True)

        # Create config and setup service
        create_config_file(port)
        subprocess.run(["loclx", "service", "uninstall"], 
                      check=True, 
                      capture_output=True)
        subprocess.run(["loclx", "service", "install", "--config", "loclx_service_config.yaml"], 
                      check=True, 
                      capture_output=True)
        subprocess.run(["loclx", "service", "start"], 
                      check=True, 
                      capture_output=True)

        time.sleep(2)  # Wait for service to start

        output = subprocess.run(["loclx", "tunnel", "list"], 
                              capture_output=True, 
                              text=True, 
                              check=True)

        logger.info(output.stdout)
        match = re.search(r'http\s+(\S+)', output.stdout)

        if match:
            url = match.group(1)
            logger.info(f"Service exposed at: https://{url}")
            return url
        else:
            logger.warning("No URL found in tunnel list output")
            return None

    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {str(e)}")
        raise TunnelError(f"Failed to start tunnel: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error starting tunnel: {str(e)}")
        raise

def http_tunnel_stop() -> None:
    """Stop HTTP tunnel"""
    try:
        logger.info("Stopping HTTP tunnel...")
        subprocess.run(["loclx", "service", "stop"], 
                      check=True, 
                      capture_output=True)
        subprocess.run(["loclx", "service", "uninstall"], 
                      check=True, 
                      capture_output=True)
        logger.info("HTTP tunnel stopped successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to stop tunnel: {str(e)}")
        raise TunnelError(f"Failed to stop tunnel: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error stopping tunnel: {str(e)}")
        raise

def http_tunnel_status() -> str:
    """Check HTTP tunnel status"""
    try:
        logger.info("Checking HTTP tunnel status...")
        output = subprocess.run(["loclx", "tunnel", "list"], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        return output.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get tunnel status: {str(e)}")
        raise TunnelError(f"Failed to get tunnel status: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error checking tunnel status: {str(e)}")
        raise