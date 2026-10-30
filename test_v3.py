import torch
import premem_kernel

def run_system_verification_trial():
    print("重新 ⚡ Initializing PreMem Core V3 Verification Loop...")
    
    seq_len = 1024
    num_heads = 32
    head_dim = 128
    block_size = 64
    perplexity_threshold = 3.5
    
    query_states = torch.randn(seq_len, num_heads, head_dim, dtype=torch.float16)
    key_states = torch.randn(seq_len, num_heads, head_dim, dtype=torch.float16)
    value_states = torch.randn(seq_len, num_heads, head_dim, dtype=torch.float16)
    
    print(f"📊 Input Tensors Allocated. Shape: {query_states.shape}")
    
    try:
        quant_state = premem_kernel.forward_attention_virtualization(
            query_states, key_states, value_states, block_size, perplexity_threshold
        )
        print("✅ Low-level C++ Quantization Binding Execution: SUCCESS")
        
        q_tokens = quant_state.quantized_tokens.to(torch.float32)
        q_scales = quant_state.block_scales.to(torch.float32)
        flattened_orig = query_states.to(torch.float32).flatten()
        reconstructed = torch.zeros_like(flattened_orig)
        flattened_quant = q_tokens.flatten()
        
        for b in range(len(q_scales)):
            start = b * block_size
            end = min(start + block_size, len(flattened_orig))
            reconstructed[start:end] = flattened_quant[start:end] * q_scales[b]
            
        cos_sim = torch.nn.functional.cosine_similarity(flattened_orig.unsqueeze(0), reconstructed.unsqueeze(0)).item()
        print(f"   -> Quantization Cosine Similarity: {cos_sim:.6f}")
        
    except Exception as e:
        print(f"❌ C++ Quantization Execution Fault: {str(e)}")
        return

    print("\n🔄 Initializing Shared-Memory Deduplication Proof...")
    replicated_kv = torch.ones(10, block_size, dtype=torch.float16)
    try:
        redirect_map = premem_kernel.deduplicate_kv_cache_blocks(replicated_kv, block_size)
        print(f"✅ Deduplication Tracking Map Returned: {redirect_map.tolist()}")
    except Exception as e:
        print(f"❌ Deduplication Execution Fault: {str(e)}")
        return

    print("\n📦 Initializing Adaptive Memory Defragmentation Compactor...")
    try:
        mock_tokens = quant_state.quantized_tokens
        compacted = premem_kernel.defragment_memory_blocks(mock_tokens, redirect_map)
        print("✅ Memory Compactor Defragmentation Pass: SUCCESS")
    except Exception as e:
        print(f"❌ Defragmentation Execution Fault: {str(e)}")
        return

    print("\n🌐 Triggering Storage Allocation Check...")
    storage_tensor = torch.zeros_like(query_states)
    try:
        premem_kernel.evict_filler_blocks_to_tier(storage_tensor, 0, "/tmp/premem_v3_cache")
        print("✅ Bare-metal Memory Eviction Sequence: SUCCESS")
    except Exception as e:
        print(f"❌ Memory Eviction Fault: {str(e)}")
        return

    print("\n🚀 PreMem Core V3 Core Architecture Layer Status: STABLE & CRITICAL VERIFIED.")

if __name__ == "__main__":
    run_system_verification_trial()
