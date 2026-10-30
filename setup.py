from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CppExtension

setup(
    name='premem_kernel',
    ext_modules=[
        CppExtension(
            name='premem_kernel',
            sources=['premem_binding.cpp', 'premem_kernel.cpp'],
            extra_compile_args=['-std=c++17']
        )
    ],
    cmdclass={'build_ext': BuildExtension}
)
