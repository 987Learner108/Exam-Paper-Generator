import os
from pathlib import Path
from setuptools import setup, find_packages

# Get the base directory
BASE_DIR = Path(__file__).parent

# Read requirements
with open(BASE_DIR / 'requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read README if it exists
try:
    with open(BASE_DIR / 'README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = 'Intelligent Exam Paper Generator with Multi-Agent AI'

setup(
    name="exam-paper-generator",
    version="1.0.0",
    packages=find_packages(where='.', exclude=['tests*']),
    install_requires=requirements,
    python_requires='>=3.9',
    author="Dinesh Gupta",
    author_email="987dineshgupta@gmail.com",
    description="Intelligent Exam Paper Generator with Multi-Agent AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/987Learner108/exam-paper-generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    include_package_data=True,
)
