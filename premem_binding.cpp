#include <torch/extension.h>
#include "premem_kernel.hpp"

namespace premem {
namespace custom_kernel {

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.doc() = "PreMem Core V3 - Low-Level Mixed Precision Attention Virtualization C++ Module";
    
    py::class_<QuantizationState>(m, "QuantizationState")
        .def_readwrite("quantized_tokens", &QuantizationState::quantized_tokens)
        .def_readwrite("block_scales", &QuantizationState::block_scales)
        .def_readwrite("sram_fp16_mask", &QuantizationState::sram_fp16_mask);

    m.def("forward_attention_virtualization", 
          &forward_attention_virtualization, 
          "Forward block-wise mixed-precision attention routing kernel (C++)",
          py::arg("query_states"),
          py::arg("key_states"),
          py::arg("value_states"),
          py::arg("block_size"),
          py::arg("perplexity_threshold"));
          
    m.def("evict_filler_blocks_to_tier", 
          &evict_filler_blocks_to_tier, 
          "Bare-metal memory register eviction check and storage dump (C++)",
          py::arg("storage_tensor"),
          py::arg("block_index"),
          py::arg("target_storage_path"));

    m.def("deduplicate_kv_cache_blocks", 
          &deduplicate_kv_cache_blocks, 
          "KV-Cache Shared-Memory Deduplication Protocol (C++)",
          py::arg("kv_states"),
          py::arg("block_size"));

    m.def("defragment_memory_blocks", 
          &defragment_memory_blocks, 
          "Adaptive Block Defragmentation Engine (C++)",
          py::arg("quantized_tokens"),
          py::arg("redirect_map"));
}

} // namespace custom_kernel
} // namespace premem
 