from setuptools import setup, find_packages

setup(
    name="assistant_api",
    version="0.1.0",
    description="A short description of my package",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        # Add any other dependencies your package needs here
    ],
)
