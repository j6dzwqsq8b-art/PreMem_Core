# =======================================================
# PROJECT: PreMem Core Memory Infrastructure (v14.0)
# MODULE: Full-Stack API Server Bridge (Phase J)
# ARCHITECTURE: Flask REST Core API Node (MacBook M1)
# =======================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from simulator import PreMemController
import os

app = Flask(__name__)
CORS(app)  # Enables cross-origin resource sharing for Safari matching

# Initialize our Phase I real machine learning controller inside the API hub
premem_node = PreMemController(max_vram_blocks=2)

@app.route('/api/status', methods=['GET'])
def get_hardware_status():
    """Exposes real-time model hardware registration matrices directly to the web dashboard."""
    try:
        active_hot = sum(1 for b in premem_node.vllm_block_table.values() if b['tier'] == 'GPU_VRAM_HOT')
        
        # Build layout inventory registry to ship to Safari
        blocks_data = {}
        for bid, meta in premem_node.vllm_block_table.items():
            blocks_data[bid] = {
                "tier": meta["tier"],
                "last_seen_ago": meta["last_seen_ago"]
            }
            
        return jsonify({
            "status": "ONLINE",
            "max_capacity": premem_node.max_vram_capacity,
            "active_hot_count": active_hot,
            "vault_files": os.listdir(premem_node.vault_path),
            "blocks": blocks_data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/prompt', methods=['POST'])
def process_ui_prompt():
    """Intercepts user prompts from Safari web interface to run live array swaps."""
    try:
        data = request.json or {}
        user_text = data.get("prompt", "").strip()
        
        if not user_text:
            return jsonify({"status": "EMPTY_PROMPT", "message": "No keystroke token bytes received."}), 400
            
        print(f"\n🌐 [API ROUTE] Incoming Safari interface packet caught: '{user_text}'")
        
        # Capture the terminal console output logs to display performance status
        premem_node.process_keystroke_buffer(user_text)
        
        # Return updated hardware status arrays directly back to the webpage UI view
        active_hot = sum(1 for b in premem_node.vllm_block_table.values() if b['tier'] == 'GPU_VRAM_HOT')
        blocks_data = {k: {"tier": v["tier"], "last_seen_ago": v["last_seen_ago"]} for k, v in premem_node.vllm_block_table.items()}
        
        return jsonify({
            "status": "PROCESSED",
            "user_prompt": user_text,
            "active_hot_count": active_hot,
            "vault_files": os.listdir(premem_node.vault_path),
            "blocks": blocks_data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("======================================================")
    print("===  PREMEM FULL-STACK API SERVER ACTIVE (PORT 5000) ===")
    print("======================================================")
    # Launch production test engine cluster node on localhost port 5000
    app.run(host='127.0.0.1', port=5000, debug=False)
