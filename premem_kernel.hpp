#pragma once
#include <torch/extension.h>
#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>

namespace premem {
namespace custom_kernel {

struct QuantizationState {
    torch::Tensor quantized_tokens;
    torch::Tensor block_scales;
    torch::Tensor sram_fp16_mask;
};

// Foundational low-overhead C++ function declarations
QuantizationState forward_attention_virtualization(
    torch::Tensor& query_states,
    torch::Tensor& key_states,
    torch::Tensor& value_states,
    const int64_t block_size,
    const float perplexity_threshold
);

void evict_filler_blocks_to_tier(
    torch::Tensor& storage_tensor,
    const int64_t block_index,
    const std::string& target_storage_path
);

// Advanced KV-Cache Shared-Memory Deduplication Protocol
torch::Tensor deduplicate_kv_cache_blocks(
    torch::Tensor& kv_states,
    const int64_t block_size
);

// Adaptive Block Defragmentation Engine
torch::Tensor defragment_memory_blocks(
    torch::Tensor& quantized_tokens,
    torch::Tensor& redirect_map
);

} // namespace custom_kernel
} // namespace premem
