from setuptools import setup, find_packages

setup(
    name="sreview",  # The name of your package
    version="0.1.0",  # Version number
    packages=find_packages(),  # Automatically find all packages in the project
    install_requires=[  # List of dependencies
        "torch",
        "transformers",
        "sentencepiece",
    ],
    author="Sandun Lakshan",
    author_email="sandunlakshan213@gmail.com",
    description="A movie review sentiment analysis model using ALBERT",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://huggingface.co/kmack/imdb-albert-calssification",  # Replace with your GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
