# loclx_colab

loclx_colab is a lightweight Python package that creates a seamless bridge between Google Colab notebooks and Localxpose service. It enables easy exposure and access to web applications running in Colab environments, making it simple to test and showcase web services directly from your Colab notebooks.

## Features

- Automatic `loclx` package installation 
- LocalXpose service management
- Create, stop and list  HTTP tunnels 

## Installation

To install the package on Colab, run:

```bash
!pip install loclx_colab

```

## Usage
Create an HTTP tunnel
```Python
import loclx_colab.loclx as lx

port = 1234 # The service port that you want to expose
access_token = "your_access_token" # Your LocalXpose token here
url = lx.http_tunnel_start(port, access_token) 
print(f"Your service is exposed to this URL: {url}")
```
Stop the HTTP tunneling service 
```Python
lx.http_tunnel_stop()
```
List HTTP tunels
```Python
lx.http_tunnel_status()
```
## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.


