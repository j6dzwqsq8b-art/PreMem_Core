# =======================================================
# PROJECT: PreMem Core Memory Simulator (v9.0)
# MODULE: Master Interactive Latency Orchestrator Shell
# ARCHITECTURE: Local Workstation Optimizer (MacBook M1)
# =======================================================

import time
import sys

# ⚙️ HARDWARE PARAMETERS
VRAM_MAX_BLOCK_CAPACITY = 3   
SSD_BUS_TRANSFER_SPEED_MS = 100  

# 💾 LIVE DATA REGISTRIES
ssd_storage_vault = ['block_02', 'block_04']  
vram_memory_strip = [1, 1, 1, 0, 0, 0, 0, 0]

vllm_block_table = {
    "block_01": {"last_seen_ago": 12, "tier": "GPU_VRAM_HOT"},
    "block_02": {"last_seen_ago": 75, "tier": "MAC_SSD_COLD"}, 
    "block_03": {"last_seen_ago": 3,  "tier": "GPU_VRAM_HOT"},
    "block_04": {"last_seen_ago": 90, "tier": "MAC_SSD_COLD"}, 
    "block_05": {"last_seen_ago": 8,  "tier": "GPU_VRAM_HOT"}, 
}

def render_hardware_progress_bar(block_name):
    print(f"⚡ [BUS TRANSFER] Routing '{block_name}': Local SSD ---> GPU VRAM")
    sys.stdout.write("                 Loading Matrix Blocks: [")
    sys.stdout.flush()
    for step in range(20):
        time.sleep(SSD_BUS_TRANSFER_SPEED_MS / 2000)
        sys.stdout.write("█")
        sys.stdout.flush()
    sys.stdout.write("] 100% FETCHED\n")

def run_background_defrag():
    global vram_memory_strip
    wasted = vram_memory_strip.count(0)
    frag_index = (wasted / len(vram_memory_strip)) * 100
    if frag_index > 20.0:
        print(f"⚡ [DEFRAG] Fragmentation at {frag_index:.1f}%. Compacting lanes...")
        vram_memory_strip = [b for b in vram_memory_strip if b == 1] + [g for g in vram_memory_strip if g == 0]
        print(f"   -> Optimized Allocation Map: {vram_memory_strip}")

print("======================================================")
print("===   PREMEM INTEGRATED REAL-TIME ORCHESTRATOR SHELL ===")
print("======================================================")
print("Commands: Type regular phrases mentioning 'block_02' or 'block_04'")
print("          Type 'status' to print live hardware telemetry readings")
print("          Type 'exit' to terminate session\n")

while True:
    user_input = input("PreMem-Master-Shell > ").strip()
    
    if user_input.lower() == 'exit':
        print("\n[SHUTDOWN] Terminating engine threads. Node securely unmounted.")
        break
        
    elif user_input.lower() == 'status':
        print("\n" + "-" * 40)
        print("📊 LIVE ENVIRONMENT MATRIX INTERFACE STATUS:")
        print(f"   -> Active GPU VRAM Blocks:  {sum(1 for b in vllm_block_table.values() if b['tier'] == 'GPU_VRAM_HOT')}")
        print(f"   -> Offloaded SSD Vault Blocks: {ssd_storage_vault}")
        print(f"   -> Hardware Memory Strip Map:  {vram_memory_strip}")
        print("-" * 40 + "\n")
        continue

    if not user_input:
        continue

    intercepted = False
    for target_block in list(ssd_storage_vault):
        if target_block in user_input:
            print(f"\n🚀 [INTERCEPT]: Target block '{target_block}' caught in text stream!")
            intercepted = True
            
            # CAPACITY VERIFICATION
            current_vram_load = sum(1 for b in vllm_block_table.values() if b['tier'] == 'GPU_VRAM_HOT')
            if current_vram_load >= VRAM_MAX_BLOCK_CAPACITY:
                active_units = {k: v for k, v in vllm_block_table.items() if v['tier'] == 'GPU_VRAM_HOT'}
                coldest_unit = max(active_units, key=lambda k: active_units[k]['last_seen_ago'])
                
                vllm_block_table[coldest_unit]["tier"] = "MAC_SSD_COLD"
                ssd_storage_vault.append(coldest_unit)
                print(f"   📦 [VRAM OVERFLOW] Auto-evicted coldest unit '{coldest_unit}' to SSD.")
            
            # ANIMATE PHYSICAL BUS TRANSFER TIMING
            render_hardware_progress_bar(target_block)
            
            # STATE UPDATE
            vllm_block_table[target_block]["tier"] = "GPU_VRAM_HOT"
            vllm_block_table[target_block]["last_seen_ago"] = 0
            ssd_storage_vault.remove(target_block)
            print(f"   ✅ [SUCCESS] '{target_block}' cached into Hot VRAM.")
            
            # DEFRAGMENT LANE SWEEP
            run_background_defrag()
            print()

    if not intercepted:
        print("✅ Command scanned. VRAM state stable. Zero swapping triggered.\n")

