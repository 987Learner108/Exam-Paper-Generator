from setuptools import setup, find_packages

setup(
    name="exam-paper-generator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    python_requires='>=3.9',
    author="Your Name",
    author_email="your.email@example.com",
    description="Intelligent Exam Paper Generator with Multi-Agent AI",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/exam-paper-generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
