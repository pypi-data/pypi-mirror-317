from setuptools import setup, find_packages

# 讀取 README.md 作為長描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mathalgo2",
    version="0.4.0",
    author="Donseking",
    author_email="0717albert@gmail.com",
    description="MathAlgo2 是一個全面的 Python 數學演算法與資料處理工具包，提供多樣化的演算法實現、視覺化功能、檔案處理工具以及數據分析功能。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Donseking/MathAlgo2",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
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
        "numpy",
        "sympy",
        "matplotlib",
        "cryptography",
        "networkx",
        "pandas",
    ],
    extras_require={
        'dev': [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5",
        ],
        'docs': [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5",
        ],
    },
)