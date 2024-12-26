from setuptools import setup, find_packages

setup(
    name="StockFactor",  # 包名
    version="0.1.0",    # 初始版本
    author="Kai",
    author_email="james2225061@gmail.com",
    description="A package with stock function",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KaiXiangC/StockFactor",
    packages=find_packages(),
    install_requires=[],  # 依赖项（可从 requirements.txt 中填充）
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Python 版本要求
)