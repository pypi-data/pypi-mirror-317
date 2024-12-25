from setuptools import setup, find_packages

setup(
    name="toothedsword",       # PyPI 上的包名
    version="0.1.0",           # 包的版本
    description="A sample package named toothedsword",
    packages=find_packages(),  # 自动发现包含 __init__.py 的包
    python_requires=">=3.6",   # 指定支持的 Python 版本
)

