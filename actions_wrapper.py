import subprocess
import requests
import time
import socket

from parse_menus import parse_week

# 1. Start the mensa-api server
cmd = [
    "nix", "develop", ".#mensa-api", "-c",
    "bash", "-c", "cd mensa-api; cargo run"
]
server_proc = subprocess.Popen(cmd)

# 2. Wait until the server is reachable
def wait_for_port(host, port, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(1)
    raise RuntimeError("Server not reachable after timeout")

wait_for_port("localhost", 3030)

# 3. Run Parsers for each Menu
parse_week()

# 4. Shut down the server
server_proc.terminate()
server_proc.wait()

