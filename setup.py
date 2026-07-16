"""Setup script for km-g15-rgb"""
from setuptools import setup, find_packages

setup(
    name="km-g15-rgb",
    version="0.1.0",
    description="AUKEY KM-G15 RGB Keyboard Control CLI",
    author="km-g15-reverse-eng",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "hidapi>=0.14.0",
        "click>=8.0",
    ],
    entry_points={
        "console_scripts": [
            "km-g15-rgb=km_g15_rgb.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
)
