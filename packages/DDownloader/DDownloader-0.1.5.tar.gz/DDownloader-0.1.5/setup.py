from setuptools import setup, find_packages

setup(
    name="DDownloader",
    version="0.1.5",
    description="A downloader for DRM-protected content.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="ThatNotEasy",
    author_email="apidotmy@proton.me",
    url="https://github.com/ThatNotEasy/DDownloader",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests",
        "coloredlogs",
        "loguru",
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "ddownloader=ddownloader.main:main",
        ],
    },
)
