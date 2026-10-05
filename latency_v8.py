# =======================================================
# PROJECT: PreMem Core Memory Simulator (v8.0)
# MODULE: Asynchronous Data Latency Engine & Progress Bus
# ARCHITECTURE: Local Workstation Optimizer (MacBook M1)
# =======================================================

import time
import sys

# ⚙️ HARDWARE SPEED & DATA LAWS
VRAM_MAX_BLOCK_CAPACITY = 3   
SSD_BUS_TRANSFER_SPEED_MS = 100  # Emulated hardware delay per memory block unit

# 💾 INTERACTIVE STORAGE DIRECTORY
ssd_storage_vault = ['block_02', 'block_04']  

vllm_block_table = {
    "block_01": {"last_seen_ago": 12, "tier": "GPU_VRAM_HOT"},
    "block_02": {"last_seen_ago": 75, "tier": "MAC_SSD_COLD"}, 
    "block_03": {"last_seen_ago": 3,  "tier": "GPU_VRAM_HOT"},
    "block_04": {"last_seen_ago": 90, "tier": "MAC_SSD_COLD"}, 
    "block_05": {"last_seen_ago": 8,  "tier": "GPU_VRAM_HOT"}, 
}

def render_hardware_progress_bar(block_name):
    """
    Simulates the physical latency delay of moving heavy context tensors 
    across the MacBook hardware bus from local SSD storage up to GPU VRAM.
    """
    print(f"⚡ [BUS TRANSFER] Initializing hardware pipeline for '{block_name}'...")
    print(f"                 Routing data lane: Local SSD ---> Apple M1 GPU VRAM")
    sys.stdout.write("                 Progress: [")
    sys.stdout.flush()
    
    # Simulate a step-by-step physical block loading sequence
    for step in range(20):
        time.sleep(SSD_BUS_TRANSFER_SPEED_MS / 2000) # Incremental millisecond clock tick
        sys.stdout.write("█")
        sys.stdout.flush()
        
    sys.stdout.write("] 100% FETCH COMPLETE\n")

print("======================================================")
print("===     PREMEM HARDWARE BUS LATENCY SIMULATOR LIVE     ===")
print("======================================================\n")

# 🔍 LIVE USER INPUT STREAM SIMULATION
# The user is mid-sentence, explicitly mentioning block_02
user_typing_stream = "Pull the attention matrices stored inside block_02"
print(f"[BUFFER] Active Input Stream Intercepted: \"{user_typing_stream}\"\n")

# 🔄 ASYNCHRONOUS INTERCEPTION LOOP
for target_block in list(ssd_storage_vault):
    if target_block in user_typing_stream:
        print(f"🚀 [INTERCEPT]: Target element '{target_block}' detected in active buffer array!")
        
        # Check if the memory tier is full
        current_vram_load = sum(1 for b in vllm_block_table.values() if b['tier'] == 'GPU_VRAM_HOT')
        
        if current_vram_load >= VRAM_MAX_BLOCK_CAPACITY:
            print(f"   ⚠️  CAPACITY WARNING: VRAM full ({current_vram_load}/{VRAM_MAX_BLOCK_CAPACITY}). Triggering eviction...")
            active_units = {k: v for k, v in vllm_block_table.items() if v['tier'] == 'GPU_VRAM_HOT'}
            coldest_unit = max(active_units, key=lambda k: active_units[k]['last_seen_ago'])
            
            # Flush memory page out
            vllm_block_table[coldest_unit]["tier"] = "MAC_SSD_COLD"
            ssd_storage_vault.append(coldest_unit)
            print(f"   📦 [EVICTION] Shuffled '{coldest_unit}' out to make structural room.\n")
        
        # ⏱️ TRIGGER THE PHYSICAL HARDWARE BUS TIMING BAR
        render_hardware_progress_bar(target_block)
        
        # Finalize the memory tier tag reallocation
        vllm_block_table[target_block]["tier"] = "GPU_VRAM_HOT"
        vllm_block_table[target_block]["last_seen_ago"] = 0
        ssd_storage_vault.remove(target_block)
        print(f"\n✅ [SUCCESS] '{target_block}' is fully cached inside GPU VRAM memory space.")

print("\n" + "-" * 54)
print("📊 HARDWARE LATENCY TERMINAL TELEMETRY LOGS:")
print(f"   -> Active hot blocks remaining inside VRAM: {sum(1 for b in vllm_block_table.values() if b['tier'] == 'GPU_VRAM_HOT')}")
print(f"   -> Cold blocks currently resting in SSD:     {ssd_storage_vault}")
print("======================================================")
