# 🛰️ PreMem Core V2: Asynchronous KV Cache Telemetry & FIFO Storage Offloader

PreMem Core V2 is an advanced, object-oriented memory optimization middleware framework designed to intercept attention layer matrices, profile KV Cache memory bloat in real-time, and dynamically execute non-blocking asynchronous storage swaps to local NVMe SSD flash storage pools. 

Designed specifically to tackle the trillion-dollar memory bottleneck in high-throughput LLM inference engines executing long multi-turn context streams.

## 🏗️ Core Architecture Spec Sheet
* **Dynamic Parameter Loading:** Intercepts real model topologies (`Qwen-0.5B-Chat` layout via Hugging Face AutoConfig) mapping exact `Hidden Dimensions (1024)` and `Layer Count (24)`.
* **Asynchronous Eviction Loop:** Leverages the native `asyncio` engine to trigger multi-threaded, non-blocking `.bin` tensor chunk serialization directly to storage when local memory breaches a 75% hardware safety ceiling.
* **Chronological FIFO Array Tracker:** Implements a true First-In-First-Out (FIFO) queue array to chronologically map memory blocks, ensuring the oldest conversation states are safely offloaded first.
* **Two-Way Cache Retrieval Engine:** Seamlessly looks up offloaded chunk addresses from a local index map registry, reads binary streams from flash storage, and reloads data vectors straight back to active memory (`RELOADED_IN_VRAM`) with zero thread lag.
* **Telemetry Web UI Infrastructure:** Exposes backend engine telemetry metrics to a local frontend dashboard through a multi-threaded Flask API server interface.

## 📁 Repository Structure
```text
PreMem_Core_V2/
├── PreMem_Core_V2/
│   ├── app.py             # Flask Web Infrastructure Telemetry Server
│   ├── simulator.py       # Asynchronous FIFO Eviction & Retrieval Core Engine
│   └── templates/
│       └── index.html     # PreMem Cluster Visual Dashboard Interface
```

## 🚀 Execution & Verification
To launch the full-stack telemetry cluster infrastructure panel locally, initialize the application path entry point via the global path runtime:
```bash
/usr/bin/python3 PreMem_Core_V2/app.py
```
Open your display dashboard terminal at `http://127.0.0.1:5001` to view live memory allocations.