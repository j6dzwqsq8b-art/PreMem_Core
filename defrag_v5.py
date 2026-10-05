# =======================================================
# PROJECT: PreMem Core Memory Simulator (v5.0)
# MODULE: Pre-Emptive Cache Defragmenter & Memory Compactor
# ARCHITECTURE: Local Workstation Optimizer (MacBook M1)
# =======================================================

import time

# 📊 SIMULATING A FRAGMENTED VRAM ARRAY LAYOUT
# A '0' represents an empty, wasted memory gap. A '1' represents allocated data.
vram_memory_strip = [1, 0, 1, 0, 1, 1, 0, 1]

print("======================================================")
print("===   PREMEM PRE-EMPTIVE DEFRAGMENTER ACTIVE       ===")
print("======================================================\n")

print(f"[INITIAL STATE] VRAM Map Layout: {vram_memory_strip}")

# 📊 Step A: Calculate Memory Fragmentation Telemetry
total_slots = len(vram_memory_strip)
allocated_slots = sum(vram_memory_strip)
wasted_gaps = vram_memory_strip.count(0)
fragmentation_index = (wasted_gaps / total_slots) * 100

print(f"[DIAGNOSTICS]  Total Runway Capacity: {total_slots} Blocks.")
print(f"               Allocated Context Data: {allocated_slots} Blocks.")
print(f"               Wasted Fragmentation Gaps: {wasted_gaps} Units.")
print(f"               Current Fragmentation Index: {fragmentation_index:.1f}%\n")

# 🚨 Step B: Pre-Emptive Compaction Enforcement Rule
# If the fragmentation gaps take up more than 20% of the strip, trigger defrag!
if fragmentation_index > 20.0:
    print("⚠️  ALERT: High memory fragmentation detected! Initiating compaction...")
    
    # PreMem Logic: Filter out all the data blocks (1s) and push all empty gaps (0s) to the end
    active_data = [block for block in vram_memory_strip if block == 1]
    cleared_gaps = [gap for gap in vram_memory_strip if gap == 0]
    
    # Compact the array structure together
    vram_memory_strip = active_data + cleared_gaps
    
    print("📦 [COMPACTION] Moving active memory pages into continuous alignment.")
    print("                Wasted gaps compressed out of the primary allocation zone.")

print("-" * 54)
print(f"📊 FINAL COMPACTED MEMORY LAYOUT STATE:")
print(f"   -> Optimized VRAM Map Runway: {vram_memory_strip}")
print("======================================================")

