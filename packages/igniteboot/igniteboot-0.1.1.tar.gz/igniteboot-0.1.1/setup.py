from setuptools import setup, find_packages

setup(
    name="igniteboot",
    version="0.1.1",
    description="A lightweight and modular Python backend framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="m3r0n9",
    author_email="your-email@example.com",
    url="https://github.com/m3r0n9/igniteboot",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "jinja2",
        "pyyaml",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "ignite=ignite.cli:main",
        ],
    },
)
