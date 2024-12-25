from setuptools import setup, find_packages

setup(
    name="ai-network-dag-sdk",
    version="0.9.4",
    author="kmh4500",
    author_email="kimminhyun@comcom.ai",
    description="SDK for AINetwork DAG interactions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kmh4500/ai-network-dag-sdk",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "grpcio",
        "grpcio-tools"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
