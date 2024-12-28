from setuptools import setup, find_packages

setup(
    name="autohint",  # Module name
    version="0.1.0",
    description="AutoHint provides real-time search suggestions with internet integration.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jai Akash",
    author_email="your_email@example.com",  # Replace with your email
    url="https://github.com/Jkdevlopments/autohint",  # Your GitHub link
    packages=find_packages(),
    install_requires=[
        "prompt-toolkit",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)