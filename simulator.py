# =======================================================
# PROJECT: PreMem Core Memory Engine (v10.0 - FINAL)
# MODULE: Physical Storage Interface & Hardware Bus Sync
# ARCHITECTURE: Local Workstation Optimizer (MacBook M1)
# =======================================================

import time
import sys
import os

# ⚙️ HARDWARE LAWS & DIRECTORY SETTING
VRAM_MAX_BLOCK_CAPACITY = 3   
SSD_BUS_TRANSFER_SPEED_MS = 100  

# Physically map the storage vault path directly onto your Mac Desktop folder
DESKTOP_VAULT_PATH = os.path.expanduser("~/Desktop/PreMem_SSD_Vault")
if not os.path.exists(DESKTOP_VAULT_PATH):
    os.makedirs(DESKTOP_VAULT_PATH)

# 💾 LIVE HARDWARE MEMORY REGISTRIES
ssd_storage_vault = []  
vram_memory_strip = [1, 1, 1, 0, 0, 0, 0, 0]  

vllm_block_table = {
    "block_01": {"tokens": "User loves coding on MacBook M1.", "last_seen_ago": 12, "tier": "GPU_VRAM_HOT"},
    "block_02": {"tokens": "PreMem core architecture thesis drawn on Page 7.", "last_seen_ago": 75, "tier": "GPU_VRAM_HOT"}, 
    "block_03": {"tokens": "Marathon training logs and physical gym anchor stats.", "last_seen_ago": 3,  "tier": "GPU_VRAM_HOT"},
}

def render_hardware_progress_bar(block_name):
    print(f"⚡ [BUS SYNC] Swapping '{block_name}': Physical Mac SSD ---> GPU VRAM")
    sys.stdout.write("                 Loading Matrix Weights: [")
    sys.stdout.flush()
    for step in range(20):
        time.sleep(SSD_BUS_TRANSFER_SPEED_MS / 2000)
        sys.stdout.write("█")
        sys.stdout.flush()
    sys.stdout.write("] 100% TRANSIT COMPLETE\n")

print("======================================================")
print("===    PREMEM PHYSICAL CORE INTEGRATION SHELL LIVE ===")
print("======================================================")
print("Commands: Type regular phrases mentioning 'block_02'")
print("          Type 'status' to audit physical desktop folders")
print("          Type 'exit' to cleanly close the engine node\n")

# Proactively scan initial table layout for cold blocks to flush to disk right away
print("[INITIALIZING] Scanning local block directory for idle elements...")
for bid, meta in list(vllm_block_table.items()):
    if meta["last_seen_ago"] > 60:
        print(f"📦 [DISK EVICTION] '{bid}' is cold. Swapping tensors to local desktop disk...")
        file_path = os.path.join(DESKTOP_VAULT_PATH, f"{bid}.txt")
        
        # Physically write the file data out to your Mac storage disk
        with open(file_path, "w") as f:
            f.write(meta["tokens"])
            
        meta["tier"] = "MAC_SSD_COLD"
        meta["tokens"] = "[OFFLOADED_TO_DISK]"
        ssd_storage_vault.append(bid)

print("🚀 Initialization complete. Interactive terminal online.\n")

while True:
    user_input = input("PreMem-Live Engine > ").strip()
    
    if user_input.lower() == 'exit':
        print("\n[SHUTDOWN] Terminating hardware links. Safe unmount complete.")
        break
        
    elif user_input.lower() == 'status':
        print("\n" + "-" * 50)
        print("📊 REAL HARDWARE ENVIRONMENT TELEMETRY:")
        print(f"   -> Active GPU VRAM Blocks: {sum(1 for b in vllm_block_table.values() if b['tier'] == 'GPU_VRAM_HOT')}")
        print(f"   -> Files sitting inside {DESKTOP_VAULT_PATH}:")
        print(f"      {os.listdir(DESKTOP_VAULT_PATH)}")
        print(f"   -> Simulated VRAM Strip Layout: {vram_memory_strip}")
        print("-" * 50 + "\n")
        continue

    if not user_input:
        continue

    intercepted = False
    for target_block in list(ssd_storage_vault):
        if target_block in user_input:
            print(f"\n🚀 [KEYSTROKE INTERCEPT]: Match for '{target_block}' caught in stream buffer!")
            intercepted = True
            
            # CAPACITY ENFORCEMENT
            current_vram_load = sum(1 for b in vllm_block_table.values() if b['tier'] == 'GPU_VRAM_HOT')
            if current_vram_load >= VRAM_MAX_BLOCK_CAPACITY:
                active_units = {k: v for k, v in vllm_block_table.items() if v['tier'] == 'GPU_VRAM_HOT'}
                coldest_unit = max(active_units, key=lambda k: active_units[k]['last_seen_ago'])
                
                # Physical Eviction: Save it out to disk before dropping from RAM
                evict_path = os.path.join(DESKTOP_VAULT_PATH, f"{coldest_unit}.txt")
                with open(evict_path, "w") as f:
                    f.write(vllm_block_table[coldest_unit]["tokens"])
                    
                vllm_block_table[coldest_unit]["tier"] = "MAC_SSD_COLD"
                vllm_block_table[coldest_unit]["tokens"] = "[OFFLOADED_TO_DISK]"
                ssd_storage_vault.append(coldest_unit)
                print(f"   📦 [VRAM OVERFLOW] Kicked '{coldest_unit}' out. Created text file on Desktop.")
            
            # ANIMATE BUS SPEED DELAY
            render_hardware_progress_bar(target_block)
            
            # PHYSICAL READ BUFFER SYNC
            target_file_path = os.path.join(DESKTOP_VAULT_PATH, f"{target_block}.txt")
            with open(target_file_path, "r") as f:
                restored_tokens = f.read()
                
            # Update local memory directory tables
            vllm_block_table[target_block]["tier"] = "GPU_VRAM_HOT"
            vllm_block_table[target_block]["tokens"] = restored_tokens
            vllm_block_table[target_block]["last_seen_ago"] = 0
            
            # Physically delete the file off your Mac hard drive since it is back in active RAM
            os.remove(target_file_path)
            ssd_storage_vault.remove(target_block)
            
            print(f"   ✅ [SYNC SUCCESS] '{target_block}' data read back to RAM. Deleted file from Desktop.\n")

    if not intercepted:
        print("✅ String processed. No disk assets referenced.\n")
