#!/usr/bin/env python3
import time, subprocess, os, logging, sys
from pathlib import Path
from datetime import datetime

METABOLISM_DIR = Path(__file__).resolve().parent
BASE_DIR = METABOLISM_DIR.parent.parent
LOG_DIR = BASE_DIR / "System/logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / f"metabolism_{datetime.now().strftime('%Y%m')}.log",
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def run_task(script_name):
    logging.info(f"Starting metabolic subtask: {script_name}")
    try:
        subprocess.run([sys.executable, str(METABOLISM_DIR / script_name)], check=True)
        logging.info(f"Task {script_name} completed successfully")
    except Exception as e:
        logging.error(f"Task {script_name} failed: {e}")

def main():
    print(f"Sovereign Metabolism Daemon started. Logs: {LOG_DIR}")
    logging.info("Sovereign Metabolism Daemon Started.")
    while True:
        run_task("purger.py")
        run_task("distiller.py")
        logging.info("Metabolism cycle complete. Sleeping 6 hours...")
        time.sleep(6 * 3600)

if __name__ == "__main__":
    main()
