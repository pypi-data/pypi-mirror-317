from setuptools import setup, find_packages

setup(
    name="toothedsword",
    version="0.1.31",
    description="nothing",
    packages=find_packages(),
    python_requires=">=3.6",
    include_package_data=True,

    package_data={
        "toothedsword": ["base/*.json", 
                         "tctb/*.json", 
                         "ningxia/*.json"],
                 },
    install_requires=[
        # "numpy>=1.12.0",
    ],
)

