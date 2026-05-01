#!/usr/bin/env python3
import os, sys, yaml, requests, json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "metabolism_config.yaml"

class Distiller:
    def __init__(self):
        with open(CONFIG_PATH, 'r') as f:
            self.config = yaml.safe_load(f)
        self.root = BASE_DIR
        self.inbox = self.root / self.config['paths']['inbox']
        self.api_url = "http://localhost:11434/api/generate"

    def log_action(self, message):
        log_path = self.root / self.config['paths']['metabolism_log']
        with open(log_path, 'a') as f:
            f.write(f"- [DISTILL] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}\n")

    def strip_sensitive(self, content):
        patterns = self.config['settings']['sensitive_patterns']
        lines = content.split('\n')
        safe_lines = []
        for line in lines:
            if any(p.lower() in line.lower() for p in patterns):
                safe_lines.append("# [REDACTED BY METABOLISM]")
            else:
                safe_lines.append(line)
        return '\n'.join(safe_lines)

    def distill_inbox(self):
        files = list(self.inbox.glob("*.md"))
        if len(files) < 1:
            return
        print(f"Distilling {len(files)} fragments from Inbox...")
        raw_contents = ""
        for f in files:
            with open(f, 'r') as fr:
                raw_contents += f"\n--- FILE: {f.name} ---\n{fr.read()}\n"
        safe_contents = self.strip_sensitive(raw_contents)
        prompt = f"""You are a senior knowledge alchemist.
Read the following Inbox fragments and crystallize them into a single,
high-quality structured knowledge document.

Requirements:
1. Remove redundancy and duplicate information.
2. Extract core logic, strategic value points, and actionable insights.
3. Use Markdown format with a clear title and structure.
4. Only keep these frontmatter fields: {self.config['settings']['allowed_frontmatter']}

Raw materials:
{safe_contents}
"""
        try:
            payload = {"model": "qwen2.5:14b", "prompt": prompt, "stream": False, "options": {"num_predict": 4096}}
            response = requests.post(self.api_url, json=payload, timeout=120)
            crystal_content = response.json().get("response")
        except Exception as e:
            print(f"API call failed: {e}")
            return
        if crystal_content:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            target_name = f"Crystallized_Knowledge_{timestamp}.md"
            target_path = self.root / "Vault/10_Projects" / target_name
            with open(target_path, 'w') as fw:
                fw.write(crystal_content)
            print(f"Distillation complete: {target_name}")
            archive_dir = self.root / self.config['paths']['archive'] / "Source_Crystals"
            archive_dir.mkdir(parents=True, exist_ok=True)
            for f in files:
                f.rename(archive_dir / f.name)
            self.log_action(f"Distilled {len(files)} fragments into {target_name}")

if __name__ == "__main__":
    d = Distiller()
    d.distill_inbox()
