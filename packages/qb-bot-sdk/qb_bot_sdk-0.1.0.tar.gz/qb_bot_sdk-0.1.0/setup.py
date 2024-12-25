from setuptools import setup, find_packages

setup(
    name="qb_bot_sdk",
    version="0.1.0",
    description="SDK for interacting with the QB Bot API",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "requests>=2.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
