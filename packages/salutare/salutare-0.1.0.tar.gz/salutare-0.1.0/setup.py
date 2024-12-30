from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="salutare",
    version="0.1.0",
    author="Tarta Daniel Nicolae",
    author_email="dannynicolaeboy87@gmail.com",
    description="A simple packet for generate a unique and safety passwords!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dannynicolae87/my_package_python_danny.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10.11',
    install_requires=[],
)
