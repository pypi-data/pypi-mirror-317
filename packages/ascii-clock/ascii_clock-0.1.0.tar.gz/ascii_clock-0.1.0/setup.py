from setuptools import setup, find_packages

setup(
    name="ascii-clock",
    version="0.1.0",
    description="A simple ASCII art clock for the terminal",
    long_description=open("README.md",encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="DynaDino",
    author_email="1725356000@qq.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "ascii-clock=ascii_clock.clock:main",
        ],
    },
)
