import torch

try:
    import triton
    import triton.language as tl
    HAS_TRITON = True
except ImportError:
    HAS_TRITON = False

def cond_triton_jit(func):
    if HAS_TRITON:
        return triton.jit(func)
    return func

@cond_triton_jit
def premem_block_quant_kernel(
    X_ptr, Y_ptr, Scales_ptr,
    stride_xb, stride_xt,
    stride_yb, stride_yt,
    BLOCK_SIZE
):
    # Establish distinct physical block program ID tracking along the GPU axis
    pid = tl.program_id(0)
    block_start = pid * BLOCK_SIZE
    
    # Generate precise pointer indexing tracks across the block grid boundary
    offsets = block_start + tl.arange(0, BLOCK_SIZE)
    x_ptrs = X_ptr + offsets
    
    # Stream token values straight out of VRAM registers into fast internal SRAM cache
    x_block = tl.load(x_ptrs)
    
    # Calculate the maximum absolute value baseline to form the quantization factor
    max_val = tl.max(tl.abs(x_block), axis=0)
    scale = max_val / 127.0  # Hard FP8 standard layout scaling denominator
    
    # Guard against zero-division errors across empty block padding allocations
    scale = tl.where(scale == 0.0, 1.0, scale)
    
    # Quantize the memory matrix elements symmetrically into signed integer scales
    quantized_block = tl.math.round(x_block / scale)

     # Direct streaming write back out to external memory registers
    y_ptrs = Y_ptr + offsets
    tl.store(y_ptrs, quantized_block.to(tl.int8))
    tl.store(Scales_ptr + pid, scale)