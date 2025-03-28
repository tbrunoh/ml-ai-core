from setuptools import setup, find_packages

# Read the version from a file (to be auto-updated in GitHub Actions)
with open("VERSION", "r") as f:
    version = f.read().strip()

setup(
    name="ml_ai_core",
    version=version,
    author="Nelson Kigen",
    author_email="nkigen@melaninluxe.ai",
    url="https://github.com/melaninluxe/ml-ai-core",
    description="Reusable PyTorch models for projects within Melanin Luxe AI organization",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0",
        "torchvision"
    ],
    python_requires=">=3.7",
)
