import threading
import subprocess
import os
import signal
import time
import sys

# Importing main functions from the other modules
from osInfo import main as osinfo_main
from predict import main as predict_main
from root import main as root_main
from ticket import main as ticket_main

# Paths to Streamlit scripts
STREAMLIT_APPS = {
    "chart": "chart.py",
    "report": "report.py",
}

# Function to run Streamlit apps as subprocesses
def run_streamlit_app(app_name):
    try:
        print(f"Starting Streamlit app: {app_name}...")
        subprocess.run(["streamlit", "run", app_name], check=True)
    except Exception as e:
        print(f"Error in Streamlit app {app_name}: {e}")

# Main function to handle threads and subprocesses
def main():
    # Create threads for the non-Streamlit modules
    threads = []
    threads.append(threading.Thread(target=osinfo_main))
    threads.append(threading.Thread(target=predict_main))
    threads.append(threading.Thread(target=root_main))
    threads.append(threading.Thread(target=ticket_main))

    # Start all threads
    for t in threads:
        t.start()

    # Start subprocesses for Streamlit apps
    processes = []
    for app, script in STREAMLIT_APPS.items():
        p = subprocess.Popen(["streamlit", "run", script])
        processes.append(p)

    try:
        # Wait for threads to complete
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("Shutting down...")

    finally:
        # Terminate Streamlit processes
        for p in processes:
            try:
                os.kill(p.pid, signal.SIGTERM)
            except OSError:
                pass
        print("All processes terminated.")

if __name__ == "__main__":
    main()
