from setuptools import setup, find_packages

setup(
    name="igniteboot",
    version="0.1.0",
    description="A lightweight and modular Python backend framework",
    author="m3r0n9",
    author_email="your-email@example.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
    ],
    entry_points={
        "console_scripts": [
            "ignite=ignite.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
