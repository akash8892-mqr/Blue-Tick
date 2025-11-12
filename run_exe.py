# run_exe.py
# Python 3.8 compatible launcher that starts the Flask app and opens the browser.
# Usage:
#   python run_exe.py
# After packaging with PyInstaller this becomes the single EXE you can double-click.

import os
import sys
import time
import socket
import webbrowser
import threading
from urllib.parse import urljoin

# If your Flask app object is in app.py and named "app", import it:
# from app import app as flask_app
# If your app factory is different, adjust import accordingly.

# ---- Try to import the Flask app ----
try:
    # prefer absolute import if this file is in same folder as app.py
    from app import app as flask_app
except Exception as e:
    print("ERROR: could not import Flask app from app.py:", e)
    sys.exit(1)

HOST = "127.0.0.1"
PORT = 5000
URL = f"http://{HOST}:{PORT}/"

def is_port_open(host, port):
    """Return True if a TCP connection can be made to host:port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.6)
    try:
        s.connect((host, port))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except Exception:
        return False
    finally:
        s.close()

def wait_for_server(host, port, timeout=10.0, poll_interval=0.2):
    """Wait until the server is listening on host:port or timeout (seconds)."""
    start = time.time()
    while time.time() - start < timeout:
        if is_port_open(host, port):
            return True
        time.sleep(poll_interval)
    return False

def start_flask():
    """Start the Flask development server. In production you would use a real server."""
    # IMPORTANT: set debug=False for bundled exe to avoid reloader creating extra processes
    flask_app.run(host=HOST, port=PORT, debug=False, use_reloader=False)

def open_browser_after_server(url, wait_timeout=10.0):
    """Wait until server is ready, then open default browser to URL."""
    ready = wait_for_server(HOST, PORT, timeout=wait_timeout)
    if not ready:
        print(f"Server not responding on {HOST}:{PORT} after {wait_timeout}s — opening browser anyway.")
    # open in a new browser window/tab
    try:
        webbrowser.open_new(url)
    except Exception as e:
        print("Failed to open browser automatically:", e)

def main():
    # start Flask server in a background thread so this process can continue and open the browser.
    server_thread = threading.Thread(target=start_flask, daemon=True)
    server_thread.start()

    # open browser (blocks until server is up or timeout)
    open_browser_after_server(URL, wait_timeout=8.0)

    # keep the main thread alive while the server is running
    try:
        while server_thread.is_alive():
            server_thread.join(timeout=0.5)
    except KeyboardInterrupt:
        print("Interrupted — exiting.")

if __name__ == "__main__":
    main()
