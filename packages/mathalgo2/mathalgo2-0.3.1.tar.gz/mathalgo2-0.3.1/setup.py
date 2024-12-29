from setuptools import setup, find_packages

# 讀取 README.md 作為長描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mathalgo2",
    version="0.3.1",
    author="Donseking",
    author_email="0717albert@gmail.com",
    description="MathAlgo2 是一個全面的 Python 數學演算法工具包，專注於提供多樣化的數學計算與演算法實現。本工具包適合研究人員、學生以及需要進行數學計算的開發者使用。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Donseking/MathAlgo2",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "scipy>=1.6.0",
        "matplotlib>=3.3.0",
        "sympy>=1.8"
    ],
)