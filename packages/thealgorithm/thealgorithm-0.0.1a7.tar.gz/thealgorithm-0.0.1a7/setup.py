from setuptools import setup, find_packages

setup(
    name="thealgorithm",
    version="0.0.1a7",
    description="AppleBoiy's algorithm package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="AppleBoiy",
    url="https://github.com/AppleBoiy/algorithm",
    packages=find_packages(include=["thealgorithm", "thealgorithm.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
