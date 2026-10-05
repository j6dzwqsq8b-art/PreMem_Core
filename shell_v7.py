# =======================================================
# PROJECT: PreMem Core Memory Simulator (v7.0)
# MODULE: Interactive User-Prompt Shell & Live Interceptor
# ARCHITECTURE: Local Workstation Optimizer (MacBook M1)
# =======================================================

import time
import sys

# ⚙️ SYSTEM PARAMETERS
VRAM_MAX_BLOCK_CAPACITY = 3   
IDLE_THRESHOLD_SECS = 60      

# 💾 LIVE DATA REGISTRIES
ssd_storage_vault = ['block_02', 'block_04']  
vram_memory_strip = [1, 0, 1, 0, 1, 0, 0, 1]  

vllm_block_table = {
    "block_01": {"last_seen_ago": 12, "tier": "GPU_VRAM_HOT"},
    "block_02": {"last_seen_ago": 75, "tier": "MAC_SSD_COLD"}, 
    "block_03": {"last_seen_ago": 3,  "tier": "GPU_VRAM_HOT"},
    "block_04": {"last_seen_ago": 90, "tier": "MAC_SSD_COLD"}, 
    "block_05": {"last_seen_ago": 8,  "tier": "GPU_VRAM_HOT"}, 
}

def check_and_defrag():
    global vram_memory_strip
    wasted = vram_memory_strip.count(0)
    frag_index = (wasted / len(vram_memory_strip)) * 100
    if frag_index > 20.0:
        print(f"\n⚡ [DEFRAG] High fragmentation detected ({frag_index:.1f}%). Compacting memory lanes...")
        vram_memory_strip = [b for b in vram_memory_strip if b == 1] + [g for g in vram_memory_strip if g == 0]
        print(f"   -> Compacted VRAM Layout Map: {vram_memory_strip}")

print("======================================================")
print("===     PREMEM INTERACTIVE SHELL ENVIRONMENT INTERRUPT   ===")
print("======================================================")
print("Commands: Type regular sentences referencing 'block_02' or 'block_04'")
print("          Type 'status' to print live hardware telemetry dashboard")
print("          Type 'exit' to terminate engine session\n")

# 🔄 INFINITE INTERACTIVE TERMINAL LOOP
while True:
    # Capture live keystroke array inputs directly from MacBook Terminal prompt
    user_input = input("PreMem-Shell > ").strip()
    
    if user_input.lower() == 'exit':
        print("\n[SHUTDOWN] Exiting PreMem Interactive Framework. Securely unmounting node...")
        sys.exit()
        
    elif user_input.lower() == 'status':
        print("\n" + "-" * 40)
        print("📊 LIVE TELEMETRY DASHBOARD READOUT:")
        print(f"   -> Active inside GPU VRAM: {sum(1 for b in vllm_block_table.values() if b['tier'] == 'GPU_VRAM_HOT')}")
        print(f"   -> Quarantined inside SSD: {ssd_storage_vault}")
        print(f"   -> Local Physical Memory Strip: {vram_memory_strip}")
        print("-" * 40 + "\n")
        continue

    if not user_input:
        continue

    # 🔍 PREDICTIVE SCANNING MODULE
    intercepted = False
    for target_block in list(ssd_storage_vault):
        if target_block in user_input:
            print(f"\n🚀 [INTERCEPT]: Detected match for '{target_block}' in raw command buffer stream!")
            intercepted = True
            
            # 🚨 CAPACITY VERIFICATION
            current_vram_load = sum(1 for b in vllm_block_table.values() if b['tier'] == 'GPU_VRAM_HOT')
            
            if current_vram_load >= VRAM_MAX_BLOCK_CAPACITY:
                active_units = {k: v for k, v in vllm_block_table.items() if v['tier'] == 'GPU_VRAM_HOT'}
                coldest_unit = max(active_units, key=lambda k: active_units[k]['last_seen_ago'])
                
                # Force Eviction Routine
                vllm_block_table[coldest_unit]["tier"] = "MAC_SSD_COLD"
                ssd_storage_vault.append(coldest_unit)
                print(f"   📦 [BUDGET LIMIT HIT] Auto-evicting unit '{coldest_unit}' down to local SSD vault.")
            
            # Complete Prefetch Execution Block
            vllm_block_table[target_block]["tier"] = "GPU_VRAM_HOT"
            vllm_block_table[target_block]["last_seen_ago"] = 0
            ssd_storage_vault.remove(target_block)
            print(f"   ✅ [ROUTING SUCCESS] '{target_block}' prefetched and restored to Hot VRAM.\n")
            
            # Run background defragmenter check loop
            check_and_defrag()
            print()

    if not intercepted:
        print("✅ Message processed. No inactive memory references detected. VRAM steady.\n")
