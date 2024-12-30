from setuptools import setup, find_packages

setup(
    name="alpha-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    author="Ray",
    author_email="xie.xinfa@gmail.com",
    description="A simple agent library for query operations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xray918/alpha-agent",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 