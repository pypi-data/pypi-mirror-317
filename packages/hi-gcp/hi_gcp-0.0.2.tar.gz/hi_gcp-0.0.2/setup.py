from setuptools import setup, find_packages

setup(
    name="hi-gcp",
    version="0.0.2",
    author="J L",
    author_email="jliu5277@gmail.com",
    description="GCP Utilities for BigQuery",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xileven",
    packages=find_packages(),
    install_requires=[
        "google-cloud-bigquery",
        "google-cloud-storage",
        "pandas",
        "pandas-gbq",
        "pyarrow",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
