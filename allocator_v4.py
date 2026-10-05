# =======================================================
# PROJECT: PreMem Core Memory Simulator (v4.0)
# MODULE: Dynamic VRAM Budget Allocator & Prefetch Router
# ARCHITECTURE: Local Workstation Optimizer (MacBook M1)
# =======================================================

import time

# ⚙️ HARDWARE CEILING PARAMETERS
VRAM_MAX_BLOCK_CAPACITY = 3   # Strict ceiling: Only 3 hot blocks allowed in VRAM
IDLE_THRESHOLD_SECS = 60      
# 💾 INITIAL MEMORY LAYER DIRECTORY
ssd_storage_vault = ['block_02', 'block_04']  

vllm_block_table = {
    "block_01": {"last_seen_ago": 12, "tier": "GPU_VRAM_HOT"},
    "block_02": {"last_seen_ago": 75, "tier": "MAC_SSD_COLD"}, # Offloaded
    "block_03": {"last_seen_ago": 3,  "tier": "GPU_VRAM_HOT"},
    "block_04": {"last_seen_ago": 90, "tier": "MAC_SSD_COLD"}, # Offloaded
    "block_05": {"last_seen_ago": 8,  "tier": "GPU_VRAM_HOT"}, # VRAM is now at 3 blocks!
}

print("======================================================")
print("===   PREMEM DYNAMIC VRAM BUDGET ALLOCATOR ACTIVE  ===")
print("======================================================\n")

# 🔍 USER INPUT STREAM MONITORING
user_input_stream = "Reference historical context data inside block_02"
print(f"[TRACKER] Input Buffer Detected: \"{user_input_stream}\"\n")

# 🔄 DYNAMIC MEMORY ROUTING ENGINE
for target_block in list(ssd_storage_vault):
    if target_block in user_input_stream:
        print(f"🚀 [INTERCEPT]: Found '{target_block}' in typing buffer.")
        
        # 📊 Step A: Mathematically calculate current active VRAM usage
        current_vram_load = sum(1 for b in vllm_block_table.values() if b['tier'] == 'GPU_VRAM_HOT')
        print(f"   [CHECK] Current VRAM Load: {current_vram_load}/{VRAM_MAX_BLOCK_CAPACITY} Blocks.")
        
        # 🚨 Step B: Hardware Budget Enforcement Rule
        if current_vram_load >= VRAM_MAX_BLOCK_CAPACITY:
            print(f"   ⚠️  CRITICAL: VRAM capacity reached! Initiating auto-eviction...")
            
            # Find the oldest/coldest active block to sacrifice (highest last_seen_ago)
            active_blocks = {k: v for k, v in vllm_block_table.items() if v['tier'] == 'GPU_VRAM_HOT'}
            coldest_active_block = max(active_blocks, key=lambda k: active_blocks[k]['last_seen_ago'])
            
            # Force Eviction
            vllm_block_table[coldest_active_block]["tier"] = "MAC_SSD_COLD"
            ssd_storage_vault.append(coldest_active_block)
            print(f"   📦 [AUTO-EVICT] Coldest active unit '{coldest_active_block}' kicked to SSD.")
        
        # Step C: Complete the Prefetch operation
        vllm_block_table[target_block]["tier"] = "GPU_VRAM_HOT"
        vllm_block_table[target_block]["last_seen_ago"] = 0  
        ssd_storage_vault.remove(target_block)
        print(f"   ✅ [SUCCESS] {target_block} safely loaded into GPU VRAM.\n")

print("-" * 54)
print(f"📊 FINAL TELEMETRY HARDWARE DASHBOARD:")
print(f"   -> Hot Units Active in GPU VRAM: {sum(1 for b in vllm_block_table.values() if b['tier'] == 'GPU_VRAM_HOT')}")
print(f"   -> Cold Units Quarantined on SSD: {ssd_storage_vault}")
print("======================================================")






