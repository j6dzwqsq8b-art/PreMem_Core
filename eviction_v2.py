import time

IDLE_THRESHOLD_SECS = 60
ssd_storage_vault = []

vllm_block_table = {
    "block_01": {"last_seen_ago": 12, "tier": "GPU_VRAM_HOT"},
    "block_02": {"last_seen_ago": 75, "tier": "GPU_VRAM_HOT"},
    "block_03": {"last_seen_ago": 3,  "tier": "GPU_VRAM_HOT"},
    "block_04": {"last_seen_ago": 90, "tier": "GPU_VRAM_HOT"},
}

for block_id, metadata in vllm_block_table.items():
    if metadata["last_seen_ago"] > IDLE_THRESHOLD_SECS:
        metadata["tier"] = "MAC_SSD_COLD"
        ssd_storage_vault.append(block_id)
        print(f"📦 Evicted: {block_id} moved to SSD.")

        print(f"Active in VRAM: {sum(1 for b in vllm_block_table.values() if b['tier'] == 'GPU_VRAM_HOT')}")
        print(f"Stored on SSD: {ssd_storage_vault}")