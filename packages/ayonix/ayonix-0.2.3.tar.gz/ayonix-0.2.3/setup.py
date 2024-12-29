from setuptools import setup, find_packages

setup(
    name="ayonix",
    version="0.2.3",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "call=src.main:main",
        ],
    },
    author="Silicon27",
    author_email="yangsilicon@gmail.com",
    description="A modern CLI program for API testing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Silicon27/call",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)