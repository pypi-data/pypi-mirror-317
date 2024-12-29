from setuptools import setup, find_packages

setup(
    name="CHENYE-STOCK-ANALYSIS",           # 包名，避免重名
    version="0.1.0",                        # 初始版本号
    author="CHEN YE",                       # 作者
    author_email="1765569066@qq.com",       # 作者邮箱
    description="A Python library for stock data analysis using BaoStock API",
    long_description=open("README.md").read(),  # 从 README.md 获取项目简介
    long_description_content_type="text/markdown",  # 指定 README 使用的格式
    url="https://github.com/CYFearless/CHENYE-STOCK-ANALYSIS",  # 项目地址，更新为你的 GitHub 项目地址
    packages=find_packages(),               # 自动发现模块
    install_requires=[
        "baostock>=0.8.8",
        "pandas>=1.3.0",
    ],
    python_requires=">=3.7",                # 支持的最低 Python 版本
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
