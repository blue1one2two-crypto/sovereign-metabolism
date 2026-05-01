#!/usr/bin/env python3
import os, sys, yaml, requests
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "metabolism_config.yaml"

class Purger:
    def __init__(self):
        with open(CONFIG_PATH, 'r') as f:
            self.config = yaml.safe_load(f)
        self.root = BASE_DIR
        self.api_url = "http://localhost:11434/api/generate"
        self.graveyard = self.root / self.config['paths']['graveyard']
        self.graveyard.mkdir(parents=True, exist_ok=True)

    def log_action(self, message):
        log_path = self.root / self.config['paths']['metabolism_log']
        with open(log_path, 'a') as f:
            f.write(f"- [PURGE] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}\n")

    def audit_and_purge(self, directory):
        dir_path = self.root / directory
        files = list(dir_path.glob("*.md"))
        if not files:
            return
        print(f"Auditing directory: {directory} ({len(files)} files)")
        file_map = {i: f for i, f in enumerate(files)}
        titles = ""
        for i, f in file_map.items():
            titles += f"ID:{i} | TITLE:{f.name}\n"
        prompt = f"""You are a system architect. Audit the following file list.
Strategic keep criteria: {self.config['strategic_focus']}
Noise/purge criteria: {self.config['noise_filters']}

Classify each as KEEP (strategic asset) or NOISE (low-entropy waste).
Return strictly in format:
0: KEEP
1: NOISE

File list:
{titles}
"""
        try:
            payload = {"model": "qwen2.5:14b", "prompt": prompt, "stream": False}
            response = requests.post(self.api_url, json=payload, timeout=60)
            res = response.json().get("response")
        except Exception as e:
            print(f"API call failed: {e}")
            return
        if res:
            for line in res.split('\n'):
                line = line.strip()
                if not line or ':' not in line: continue
                try:
                    parts = line.split(':')
                    idx = int(parts[0].replace("ID", "").strip())
                    category = parts[1].strip().upper()
                    if idx in file_map and "NOISE" in category:
                        target_file = file_map[idx]
                        print(f"   => Purging noise: {target_file.name}")
                        target_file.rename(self.graveyard / target_file.name)
                        self.log_action(f"Moved {target_file.name} to Graveyard (Noise)")
                except: continue

if __name__ == "__main__":
    p = Purger()
    p.audit_and_purge("Vault/00_Inbox")
