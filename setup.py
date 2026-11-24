from setuptools import setup, find_packages

# Read the version from a file (to be auto-updated in GitHub Actions)
with open("VERSION", "r") as f:
    version = f.read().strip()

# Read the requirements from the Requirements.txt file
with open("Requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="mlaicore",
    version=version,
    author="Nelson Kigen",
    url="https://github.com/tbrunoh/ml-ai-core",
    description="Shared PyTorch models and utilities for Inclusive Skin AI",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.7",
    include_package_data=True
)
