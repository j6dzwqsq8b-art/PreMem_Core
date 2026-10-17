import os
import sys
import time
import asyncio
from flask import Flask, render_template, request, jsonify
from transformers import AutoConfig

# Force python to read local path dependencies cleanly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Re-use our validated Phase 1 architecture directly as the backend data driver
from simulator import PreMemController, KVCacheTelemetry

class DashboardController(PreMemController):
    def __init__(self):
        super().__init__()
        self.telemetry = KVCacheTelemetry(hardware_max_mb=128.0)
        self.chunk_counter = 0
        self.current_sequence_index = 0
        self.simulated_sequences = [512, 1024, 2048, 4096, 8192]
        self.is_running = False

    def get_latest_metrics(self):
        """Calculates snapshot memory metrics for the frontend interface."""
        seq = self.simulated_sequences[min(self.current_sequence_index, len(self.simulated_sequences)-1)]
        layer_bytes = 2 * 1 * seq * self.hidden_dim * 2
        total_cache_bytes = layer_bytes * self.num_layers
        total_cache_mb = total_cache_bytes / (1024 * 1024)
        usage_pct = (total_cache_mb / self.telemetry.hardware_max_mb) * 100

        return {
            "step": self.telemetry.step,
            "sequence_length": seq,
            "hidden_size": self.hidden_dim,
            "num_layers": self.num_layers,
            "active_cache_mb": round(total_cache_mb, 4),
            "max_hardware_mb": self.telemetry.hardware_max_mb,
            "capacity_load_pct": round(usage_pct, 2),
            "fifo_queue": list(self.fifo_eviction_queue),
            "registry_map": {k: v["status"] for k, v in self.cache_index_map.items()}
        }

    async def step_simulation_async(self):
        """Executes a single chronological context step calculation non-blockingly."""
        if self.current_sequence_index >= len(self.simulated_sequences):
            self.is_running = False
            return False

        seq = self.simulated_sequences[self.current_sequence_index]
        
        evac_flag = self.telemetry.profile_context_step(
            sequence_length=seq,
            hidden_size=self.hidden_dim,
            num_layers=self.num_layers
        )

        if evac_flag:
            self.chunk_counter += 1
            await self.evict_token_chunk_async(
                chunk_id=self.chunk_counter,
                sequence_length=seq,
                hidden_size=self.hidden_dim
            )
            
            if self.chunk_counter == 3:
                await self.retrieve_token_chunk_async(chunk_id=1)

        self.current_sequence_index += 1
        return True

# Initialize single backend controller instance across web worker routes
core_hub = DashboardController()

@app.route("/")
def home():
    """Serves your pre-designed local telemetry frontend dashboard html."""
    try:
        return render_template("index.html")
    except Exception:
        return """
        <html>
            <head><title>PreMem Core V2 Telemetry</title><meta http-equiv='refresh' content='2'></head>
            <body style='background:#0d1117; color:#c9d1d9; font-family:sans-serif; padding:40px;'>
                <h2>🛰️ PreMem Core V2 Telemetry Active Hub</h2>
                <hr style='border-color:#30363d;'>
                <p><b>Model:</b> Qwen-0.5B-Chat</p>
                <p><b>Pipeline State:</b> Phase 2 Data Stream Open</p>
                <p><b>Live Dashboard Analytics Payload:</b></p>
                <pre style='background:#161b22; padding:20px; border-radius:6px; border:1px solid #30363d;'>%s</pre>
            </body>
        </html>
        """ % core_hub.get_latest_metrics()

@app.route("/api/query", methods=["POST"])
def query():
    """Maintains your original endpoint while linking incoming queries to text packets."""
    data = request.json or {}
    user_input = data.get("text", "")
    print(f"\n📺 [API ROUTE] Incoming packet caught: {user_input}")
    
    # Process a step in the background when a user queries the dashboard
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(core_hub.step_simulation_async())
    loop.close()
    
    return jsonify({
        "status": "success", 
        "message": "Received",
        "metrics": core_hub.get_latest_metrics()
    })

@app.route("/api/telemetry")
def telemetry_api():
    """Polled data route delivering fresh metrics payloads instantly to the UI page layer."""
    return jsonify(core_hub.get_latest_metrics())

if __name__ == "__main__":
    print("\n🚀 LAUNCHING PREMEM CORE V2 TELEMETRY HUB ON LOCALHOST")
    print("================================================================")
    app.run(host="127.0.0.1", port=5001, debug=True)
