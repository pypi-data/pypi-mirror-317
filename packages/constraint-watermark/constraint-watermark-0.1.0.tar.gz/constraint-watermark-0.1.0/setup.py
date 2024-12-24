from setuptools import setup, find_packages

setup(
    name="constraint-watermark",
    version="0.1.0",
    description="A library for watermarking large language models via a sliding window frequency constraint through constrained decoding.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author="Aadit Juneja",
    author_email="aadit.juneja12@gmail.com",
    url="https://github.com/ajuneja23/constrained-inference",
    license="MIT",
    install_requires=[
        "torch>=1.9",
        "transformers>=4.31",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
