from setuptools import setup, find_packages

setup(
    name="atar",
    version="1.0.2",
    description="A CLI tool for AI tasks such as dataset handling, training, and validation.",
    author="MOUHIB Otman",
    author_email="mouhib.otm@gmail.com",
    url="https://github.com/otman-dev/atar-cli",  # Replace with your GitHub repo URL
    packages=find_packages(where=".", exclude=["tests*"]),
    install_requires=[
        # Add any dependencies here
        "ultralytics",  # YOLO and related tools
        "roboflow",  # Roboflow Python API
        "supervision",  # Supervision tools for vision tasks
        # Other required libraries
    ],
    entry_points={
        "console_scripts": [
            "atar-cli=atar.cli:main",  # Command to invoke your CLI
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
