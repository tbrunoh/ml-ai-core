from setuptools import setup, find_packages
import subprocess

# Read the version from a file (to be auto-updated in GitHub Actions)
def get_version():
    try:
        # Get latest git tag
        version = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"]).decode("utf-8").strip()
    except Exception:
        version = "0.1.0"  # Default if no tags exist
    return version
setup(
    name="ml_ai_core",
    version=get_version(),
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
