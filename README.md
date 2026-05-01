# 🧬 Sovereign System Metabolism

> An AI-powered autonomous knowledge distillation and entropy management framework.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MiMo Compatible](https://img.shields.io/badge/MiMo-V2.5--Pro-orange.svg)](https://platform.xiaomimimo.com)

## 🌊 What is System Metabolism?

Inspired by biological metabolism, this framework treats your knowledge base as a **living organism** that needs continuous nourishment, distillation, and waste removal to stay healthy.

Just as a human body breaks down food into nutrients (anabolism) and expels waste (catabolism), this system:

- **Distills** raw information fragments into crystallized, high-value knowledge
- **Purges** low-entropy noise and redundant data to prevent knowledge rot
- **Pulses** — a heartbeat daemon that monitors system health and triggers metabolic cycles

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│              Metabolic Daemon               │
│           (daemon.py — 6h cycle)            │
├─────────────┬───────────────────────────────┤
│   Purger    │         Distiller             │
│ (purger.py) │       (distiller.py)          │
│             │                               │
│ AI-powered  │  AI-powered knowledge         │
│ noise audit │  crystallization from         │
│ & removal   │  raw inbox fragments          │
├─────────────┴───────────────────────────────┤
│           Metabolic Pulse                   │
│        (metabolic_pulse.py)                 │
│                                             │
│  System heartbeat — monitors GPU/CPU load,  │
│  throttles background tasks during          │
│  high-priority workloads (e.g. ComfyUI)     │
└─────────────────────────────────────────────┘
```

## 📂 Project Structure

```
sovereign-metabolism/
├── metabolic_pulse.py      # System heartbeat & resource monitor
├── distiller.py            # Knowledge crystallization engine
├── purger.py               # Entropy auditor & noise removal
├── daemon.py               # Long-running metabolism daemon
├── metabolism_config.yaml  # Strategic configuration
└── README.md
```

## ⚙️ Components

### 🫀 Metabolic Pulse (`metabolic_pulse.py`)
The system's heartbeat. Runs every 60 seconds to:
- Monitor CPU/Memory/GPU utilization
- Detect high-priority GPU tasks (e.g., ComfyUI image generation)
- Switch between `NORMAL_MODE` and `EXCLUSIVE_MODE`
- Trigger metabolic cycles when the system is idle

### 🧪 Distiller (`distiller.py`)
The knowledge alchemist. When triggered:
- Scans the `Inbox` directory for raw markdown fragments
- Strips sensitive information (API keys, tokens, passwords)
- Sends content to a local LLM (Ollama/Qwen) for intelligent summarization
- Produces a single "Crystallized Knowledge" document
- Archives source materials for traceability

### 🗑️ Purger (`purger.py`)
The entropy auditor. Performs AI-driven triage:
- Evaluates files against **strategic focus areas** (AI/LLM, system architecture, finance)
- Identifies **noise** (trivial logs, outdated docs, low-quality prompts)
- Moves noise to the `Graveyard` directory
- Logs all actions for audit trail

### 🐙 Daemon (`daemon.py`)
The metabolism orchestrator. Runs continuously:
- Executes Purger → Distiller in sequence
- Sleeps 6 hours between cycles
- Maintains structured logs outside the knowledge vault

## 🛡️ Security Features

- **Automatic redaction** of sensitive patterns (`key`, `token`, `password`, `secret`, `sk-`)
- **Configurable noise filters** to prevent information overload
- **Audit logging** for all metabolic actions
- **Graceful degradation** when AI backends are unavailable

## 🚀 Quick Start

```bash
git clone https://github.com/blue1one2two-crypto/sovereign-metabolism.git
cd sovereign-metabolism
pip install psutil pyyaml requests

# Configure paths
vim metabolism_config.yaml

# Run the daemon
python daemon.py
```

## 🤖 AI Backend

Currently supports:
- **Ollama** (local) — Default backend using Qwen 2.5 14B
- **Xiaomi MiMo V2.5** — Cloud-based alternative via OpenAI-compatible API
- Extensible to any OpenAI-compatible endpoint

## 📜 License

MIT License — See [LICENSE](LICENSE) for details.

---

*"A system that cannot metabolize its own waste will eventually drown in entropy."*
