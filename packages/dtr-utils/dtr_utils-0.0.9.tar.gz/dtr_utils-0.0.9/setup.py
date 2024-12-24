from setuptools import setup, find_packages

setup(
    name="dtr_utils",  # Package name
    version="0.0.9",  # Version
    description="Utilities for Decoding Time RAG (DTR) tasks",  # Short description
    author="Rajarshi Roy",  # Your name
    author_email="royrajarshi0123@gmail.com",  # Your email
    # url="https://github.com/yourusername/dtr_utils",  # Repository URL
    packages=find_packages(),  # Automatically find sub-packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version
    install_requires=[
        # "torch==1.12.0",
        # "torch==2.5.1",
        # "transformers==4.46.3",
        # "accelerate==1.1.1",
        "nltk==3.9.1",
        # "seaborn==0.13.2",
        # "scipy==1.13.1",
        "anytree==2.12.1",
        "graphviz==0.20.3",
        "stanza==1.9.2",
        # "spacy==3.7.5",
        # "beautifulsoup4==4.12.3",
        "lxml==5.3.0",
        "googlesearch-python==1.2.5",  # For Google search functionality
        # "huggingface_hub<= 0.25.2",
    ],
)
