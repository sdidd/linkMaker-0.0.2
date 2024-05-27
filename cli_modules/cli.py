# cli_modules/cli.py

import subprocess
import signal
import os
import multiprocessing
import time
# from daemon.pidfile import TimeoutPIDLockFile
# import daemon
from cli_modules.utils import start_ngrok, store_pid, is_process_running, printUrls
from cli_modules.app import app

PID_FILE = os.path.join(os.path.dirname(__file__), 'flask_pid.txt')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'output.log')

# start_ngrok()
# app.run(host='0.0.0.0', port=5000)
# printUrls()
def start_ngrok_wrapper():
    with open(OUTPUT_FILE, 'a') as f:
        f.write("Starting ngrok...\n")
    start_ngrok()

def start_flask_app():
    with open(OUTPUT_FILE, 'a') as f:
        f.write("Starting Flask app...\n")
    app.run(host='0.0.0.0', port=5000)

def print_urls():
    with open(OUTPUT_FILE, 'a') as f:
        f.write("Printing URLs...\n")
    printUrls()

def start():
    global p1, p2, p3
    print("Press ctrl+C to terminate server")

    # Start ngrok in a subprocess
    p1 = multiprocessing.Process(target=start_ngrok_wrapper)
    p1.start()

    # Start Flask app in a subprocess
    p2 = multiprocessing.Process(target=start_flask_app)
    p2.start()

    # Start printUrls in a subprocess
    p3 = multiprocessing.Process(target=print_urls)
    p3.start()

    # Register signal handlers
    signal.signal(signal.SIGINT, terminate_processes)
    signal.signal(signal.SIGTERM, terminate_processes)
    

    try:
        # Wait indefinitely until termination signals are received
        signal.pause()
    except KeyboardInterrupt:
        pass

def terminate_processes(signum, frame):
    print("Terminating subprocesses...")
    # Terminate the subprocesses
    p1.terminate()
    p2.terminate()
    p3.terminate()

    # Join subprocesses to ensure they are fully terminated
    p1.join()
    p2.join()
    p3.join()

    # Exit the main process
    print("All subprocesses terminated.")
    exit(0)

def stop():
    print("Stopping Flask server...")
    try:
        with open(PID_FILE, 'r') as f:
            flask_pid = int(f.read().strip())
            os.kill(flask_pid, 15)  # Send SIGTERM signal
            print("Flask server stopped.")
    except FileNotFoundError:
        print("Flask PID file not found. Flask server may not be running.")
    except ProcessLookupError:
        print("Flask server process not found. It may have already stopped.")
    finally:
        try:
            os.remove(PID_FILE)  # Remove the PID file
        except FileNotFoundError:
            pass  # PID file may have been already removed