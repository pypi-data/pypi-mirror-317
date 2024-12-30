import sys
from setuptools import setup
from Cython.Build import cythonize
from distutils.extension import Extension

# 根据平台设置库文件路径和名称
if sys.platform == "win32":
    libraries = ["hs"]
    extra_link_args = []
    package_data = {"pyhyperscan": ["hs.dll", "hs_runtime.dll"]}
elif sys.platform == "linux":
    libraries = ["hs"]
    extra_link_args = ["-Llib"]
    package_data = {"pyhyperscan": ["libhs.so"]}
elif sys.platform == "darwin":
    libraries = ["hs"]
    extra_link_args = ["-Llib"]
    package_data = {"pyhyperscan": ["libhs.dylib"]}
else:
    raise RuntimeError(f"Unsupported platform: {sys.platform}")

# 定义扩展模块
ext_modules = [
    Extension(
        "pyhyperscan.pyhyperscan",  # 模块名称
        sources=["pyhyperscan/pyhyperscan.pyx"],  # Cython 源文件
        include_dirs=["include"],  # 头文件路径
        library_dirs=["lib"],  # 库文件路径
        libraries=libraries,  # 库名称
        extra_link_args=extra_link_args,  # 额外的链接参数
    )
]

setup(
    name="pyhyperscan",
    version="0.1.5",
    author="fgc",
    author_email="13654918696@163.com",
    description="A Python wrapper for Hyperscan",
    long_description=open("README.md", encoding='utf8').read(),
    long_description_content_type="text/markdown",
    url="https://gitee.com/fgc1/regex_engine_py.git",
    packages=["pyhyperscan"],
    ext_modules=cythonize(ext_modules),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8"
    ],
    python_requires=">=3.8",
    install_requires=[
        "Cython>=0.29.0",
    ],
    package_data=package_data,  # 包含动态库
)