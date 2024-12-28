from setuptools import setup, find_packages

setup(
    name='taler_shared',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "certifi>=2024.2.2,<2025.0.0",
        "pydantic>=1.8.0,<2.0.0",
        "requests>=2.31.0,<3.0.0",
        "setuptools>=70.0.0,<75.0.0",
    ],
)