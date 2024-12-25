from setuptools import setup, find_packages

setup(
    name="toothedsword",
    version="0.1.8",
    description="代码工程化",
    packages=find_packages(),
    python_requires=">=3.6",
    include_package_data=True,

    package_data={
        "toothedsword": ["base/*.json", "tctb/*.json", "ningxia/*.json"],
                 },
    install_requires=[
        # "numpy>=1.12.0",
    ],
)

