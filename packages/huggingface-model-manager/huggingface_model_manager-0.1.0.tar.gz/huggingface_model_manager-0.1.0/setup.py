from setuptools import setup, find_packages

setup(
    name="huggingface_model_manager",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for saving, loading, and using Hugging Face models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AnishKMBtech/huggingface_model_manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)