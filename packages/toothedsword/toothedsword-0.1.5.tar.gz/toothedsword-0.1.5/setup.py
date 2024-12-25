from setuptools import setup, find_packages

setup(
    name="toothedsword",
    version="0.1.5",
    description="代码工程化",
    packages=find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        "toothedsword": ["base/*.json"],
        "toothedsword": ["tctb/*.json"],
        "toothedsword": ["ningxia/*.json"],
    },
    install_requires=[
        # "numpy>=1.12.0",
    ],
)

