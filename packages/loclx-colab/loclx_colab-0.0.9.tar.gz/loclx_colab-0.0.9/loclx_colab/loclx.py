from .utils2 import is_loclx_installed, install_deb_package, create_config_file
import subprocess, os, time, re
import logging
from typing import Optional

class LoclxError(Exception):
    """Base exception for loclx errors"""
    pass

class LoginError(LoclxError):
    """Raised when login fails"""
    pass

class TunnelError(LoclxError):
    """Raised when tunnel operations fail"""
    pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_status() -> bool:
    try:
        if not is_loclx_installed():
            install_deb_package()
            return check_status()
            
        result = subprocess.run(["loclx", "a", "status"], capture_output=True, text=True)
        if "Error: you are not logged in" in result.stdout:
            logger.warning("Not logged in")
            return False
        logger.info("Successfully logged in")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to check status: {str(e)}")
        raise LoclxError(f"Status check failed: {str(e)}")

def login(access_token: str) -> None:
    if not access_token:
        raise LoginError("Access token cannot be empty")
    try:
        if not is_loclx_installed():
            install_deb_package()
            login(access_token)
        else:
            logger.info("Logging in...")
            os.environ['ACCESS_TOKEN'] = access_token
            if not check_status():
                raise LoginError("Login failed")
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise LoginError(f"Login failed: {str(e)}")

def http_tunnel_start(port: int, access_token: str) -> Optional[str]:
    if not isinstance(port, int) or port < 1 or port > 65535:
        raise ValueError("Invalid port number")
    
    try:
        if not check_status():
            login(access_token)
        
        logger.info(f"Creating HTTP tunnel on port {port}...")
        subprocess.run(["sudo", "loclx", "service", "stop"], check=True)
        create_config_file(port)
        
        for cmd in [
            ["loclx", "service", "uninstall"],
            ["loclx", "service", "install", "--config", "loclx_service_config.yaml"],
            ["loclx", "service", "start"]
        ]:
            subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start HTTP tunnel: {str(e)}")
        raise TunnelError(f"HTTP tunnel start failed: {str(e)}")
    