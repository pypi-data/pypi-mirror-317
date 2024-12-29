from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pb_assistant",
    version="1.0.1",
    author="Priyanshu Bhatt",
    author_email="priyanshubhatt80@gmail.com",
    description="A Python library to answer questions based on given data and additional queries using Gemini.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FalconX80/pb_assistant",  # Update with your GitHub URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "google-generativeai",
    ],
)
