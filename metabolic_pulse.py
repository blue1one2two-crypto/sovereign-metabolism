#!/usr/bin/env python3
import os, sys, time, psutil, subprocess, json, yaml
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = BASE_DIR / "System/Infra/sovereign-infra/scripts"
METABOLISM_DIR = BASE_DIR / "System/Metabolism"
CONFIG_PATH = METABOLISM_DIR / "metabolism_config.yaml"

class MetabolicPulse:
    def __init__(self):
        self.load_config()
        self.state_file = METABOLISM_DIR / "pulse_state.json"
        self.pulse_interval = 60
        self.active_processes = {}

    def load_config(self):
        with open(CONFIG_PATH, 'r') as f:
            self.config = yaml.safe_load(f)

    def log(self, message):
        log_path = BASE_DIR / self.config['paths']['metabolism_log']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_path, 'a') as f:
            f.write(f"- [PULSE] {timestamp} {message}\n")
        print(f"[{timestamp}] {message}")

    def check_gpu_priority(self):
        is_comfy_active = False
        for proc in psutil.process_iter(['name']):
            if 'comfyui' in proc.info['name'].lower():
                is_comfy_active = True
                break
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if sock.connect_ex(('127.0.0.1', 8188)) == 0:
                is_comfy_active = True
            sock.close()
        except: pass
        return is_comfy_active

    def get_system_load(self):
        return {"cpu": psutil.cpu_percent(interval=1), "memory": psutil.virtual_memory().percent}

    def update_state(self, is_gpu_busy):
        state = {"last_pulse": time.time(), "gpu_busy": is_gpu_busy,
                 "load": self.get_system_load(),
                 "status": "EXCLUSIVE_MODE" if is_gpu_busy else "NORMAL_MODE"}
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
        return state

    def manage_routine_tasks(self, is_gpu_busy):
        if is_gpu_busy:
            self.log("High-priority GPU task detected. Throttling routine metabolism...")
        else:
            self.run_metabolism_cycle()

    def run_metabolism_cycle(self):
        inbox_path = BASE_DIR / self.config['paths']['inbox']
        files = list(inbox_path.glob("*.md"))
        if len(files) > 5:
            self.log(f"Metabolizing {len(files)} files from Inbox...")
            subprocess.Popen(["python3", str(METABOLISM_DIR / "distiller.py")])

    def beat(self):
        self.log("Metabolic Pulse initiated.")
        try:
            while True:
                is_gpu_busy = self.check_gpu_priority()
                state = self.update_state(is_gpu_busy)
                self.manage_routine_tasks(is_gpu_busy)
                time.sleep(self.pulse_interval)
        except KeyboardInterrupt:
            self.log("Metabolic Pulse stopped by user.")
        except Exception as e:
            self.log(f"CRITICAL ERROR in Pulse: {str(e)}")

if __name__ == "__main__":
    pulse = MetabolicPulse()
    pulse.beat()
