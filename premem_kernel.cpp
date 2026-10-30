#include "premem_kernel.hpp"
#include <iostream>
#include <fstream>
#include <future>
#include <cmath>
#include <algorithm>

namespace premem {
namespace custom_kernel {

QuantizationState forward_attention_virtualization(
    torch::Tensor& query_states,
    torch::Tensor& key_states,
    torch::Tensor& value_states,
    const int64_t block_size,
    const float perplexity_threshold
) {
    // 1. Force conversion to a continuous CPU layout for localized element parsing
    torch::Tensor cpu_q = query_states.to(torch::kCPU).to(torch::kFloat32).contiguous();
    float* q_ptr = cpu_q.data_ptr<float>();
    int64_t total_elements = cpu_q.numel();

    // 2. Allocate output tensor frameworks
    torch::Tensor quantized_tokens = torch::zeros_like(query_states, torch::TensorOptions().dtype(torch::kInt8));
    int8_t* out_ptr = quantized_tokens.data_ptr<int8_t>();

    // Calculate how many distinct memory blocks sit on the data grid axis
    int64_t num_blocks = (total_elements + block_size - 1) / block_size;
    torch::Tensor block_scales = torch::zeros({num_blocks}, torch::TensorOptions().dtype(torch::kFloat32));
    float* scales_ptr = block_scales.data_ptr<float>();

    // 3. Mathematical execution loop: Scale down blocks sequentially (C++ Fallback Match)
    for (int64_t b = 0; b < num_blocks; ++b) {
        int64_t start_idx = b * block_size;
        float max_val = 0.0f;

        // Isolate the absolute maximum element factor inside the current block window
        for (int64_t i = 0; i < block_size && (start_idx + i) < total_elements; ++i) {
            float abs_val = std::abs(q_ptr[start_idx + i]);
            if (abs_val > max_val) {
                max_val = abs_val;
            }
        }

        // Calculate the symmetric quantization denominator matching FP8/Int8 layouts
        float scale = max_val / 127.0f;
        if (scale == 0.0f) scale = 1.0f;
        scales_ptr[b] = scale;

        // Compress elements inside the active block window down to signed 8-bit registers
        for (int64_t i = 0; i < block_size && (start_idx + i) < total_elements; ++i) {
            float rounded_val = std::round(q_ptr[start_idx + i] / scale);
            out_ptr[start_idx + i] = static_cast<int8_t>(std::min(std::max(rounded_val, -128.0f), 127.0f));
        }
    }

    // 4. Form low-overhead hardware tracking structures
    auto options = torch::TensorOptions().dtype(torch::kFloat16).device(query_states.device());
    torch::Tensor sram_mask = torch::ones({query_states.size(0)}, options);
    
    return QuantizationState{
        quantized_tokens.to(query_states.device()), 
        block_scales.to(query_states.device()), 
        sram_mask
    };
}

void evict_filler_blocks_to_tier(
    torch::Tensor& storage_tensor,
    const int64_t block_index,
    const std::string& target_storage_path
) {
    // Force complete down-casting conversion to Float32 on CPU before byte conversion
    torch::Tensor cpu_tensor = storage_tensor.to(torch::kCPU).to(torch::kFloat32).contiguous();
    float* data_ptr = cpu_tensor.data_ptr<float>();
    size_t byte_size = cpu_tensor.nbytes();

    // Fire an asynchronous background thread to dump memory off the active context loop
    std::async(std::launch::async, [=]() {
        std::ofstream disk_file(target_storage_path + "_block_" + std::to_string(block_index) + ".bin", std::ios::binary);
        if (disk_file.is_open()) {
            disk_file.write(reinterpret_cast<const char*>(data_ptr), byte_size);
            disk_file.close();
            std::cout << "🌐 [PreMem Async] Block " << block_index << " successfully streamed to disk." << std::endl;
        } else {
            std::cerr << "⚠️ [PreMem Fault] Failed to open asynchronous storage track path." << std::endl;
        }
    });
}

torch::Tensor deduplicate_kv_cache_blocks(
    torch::Tensor& kv_states,
    const int64_t block_size
) {
    torch::Tensor cpu_kv = kv_states.to(torch::kCPU).to(torch::kFloat32).contiguous();
    float* kv_ptr = cpu_kv.data_ptr<float>();
    int64_t total_elements = cpu_kv.numel();
    int64_t num_blocks = (total_elements + block_size - 1) / block_size;
    
    std::unordered_map<float, int64_t> unique_block_map;
    torch::Tensor redirect_map = torch::zeros({num_blocks}, torch::TensorOptions().dtype(torch::kInt64));
    int64_t* redirect_ptr = redirect_map.data_ptr<int64_t>();
    int64_t unique_count = 0;

    for (int64_t b = 0; b < num_blocks; ++b) {
        int64_t start_idx = b * block_size;
        float block_hash = 0.0f;
        for (int64_t i = 0; i < block_size && (start_idx + i) < total_elements; ++i) {
            block_hash += kv_ptr[start_idx + i];
        }
        if (unique_block_map.find(block_hash) != unique_block_map.end()) {
            redirect_ptr[b] = unique_block_map[block_hash];
        } else {
            unique_block_map[block_hash] = b;
            redirect_ptr[b] = b;
            unique_count++;
        }
    }
    std::cout << "🌐 [PreMem Deduplication] Scan complete. Found " << unique_count 
              << " unique blocks out of " << num_blocks << " total frames." << std::endl;
    return redirect_map.to(kv_states.device());
}

torch::Tensor defragment_memory_blocks(
    torch::Tensor& quantized_tokens,
    torch::Tensor& redirect_map
) {
    torch::Tensor cpu_tokens = quantized_tokens.to(torch::kCPU).to(torch::kInt8).contiguous();
    torch::Tensor cpu_map = redirect_map.to(torch::kCPU).to(torch::kInt64).contiguous();
    
    int64_t num_blocks = cpu_map.size(0);
    int64_t total_elements = cpu_tokens.numel();
    int64_t block_size = total_elements / num_blocks;
    
    int8_t* tokens_ptr = cpu_tokens.data_ptr<int8_t>();
    int64_t* map_ptr = cpu_map.data_ptr<int64_t>();
    
    torch::Tensor compacted_tokens = torch::zeros_like(quantized_tokens);
    int8_t* comp_ptr = compacted_tokens.data_ptr<int8_t>();
    int64_t written_blocks = 0;
    std::unordered_map<int64_t, int64_t> old_to_new_index;
    
    for (int64_t b = 0; b < num_blocks; ++b) {
        int64_t target_parent = map_ptr[b];
        if (old_to_new_index.find(target_parent) == old_to_new_index.end()) {
            old_to_new_index[target_parent] = written_blocks;
            int64_t source_offset = target_parent * block_size;
            int64_t dest_offset = written_blocks * block_size;
            std::copy(tokens_ptr + source_offset, tokens_ptr + source_offset + block_size, comp_ptr + dest_offset);
            written_blocks++;
        }
    }
    std::cout << "🌐 [PreMem Defragmentation] Compaction pass stable. Shrinkage factor: " 
              << num_blocks << " blocks -> " << written_blocks << " contiguous blocks." << std::endl;
    return compacted_tokens.to(quantized_tokens.device());
}

} // namespace custom_kernel
} // namespace premem
