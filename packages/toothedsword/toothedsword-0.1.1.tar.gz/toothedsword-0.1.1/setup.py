from setuptools import setup, find_packages

setup(
    name="toothedsword",       # PyPI 上的包名
    version="0.1.1",           # 包的版本
    description="A sample package named toothedsword",
    packages=find_packages(),  # 自动发现包含 __init__.py 的包
    python_requires=">=3.6",   # 指定支持的 Python 版本
    package_data={               # 明确指定需要包含的文件
        "toothedsword": ["base/*"],  # 包含 base 文件夹里的所有内容
    },
)

