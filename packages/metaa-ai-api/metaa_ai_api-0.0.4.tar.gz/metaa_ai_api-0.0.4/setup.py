from setuptools import setup, find_packages

setup(
    name="metaa-ai-api",                           # Package name
    version="0.0.4",                         # Version
    description="A package for MetaAI interaction.",
    author="Shubham",                      # Your name
    author_email="Shub76ham@gmail.com",   # Your email
    url="https://github.com/Sm7-git",      # Optional GitHub URL
    packages=find_packages(),                # Automatically find submodules
    install_requires=["huggingface-hub"],    # Required dependencies
    python_requires=">=3.7",                 # Minimum Python version
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=open("README.md").read(),  # README as PyPI description
    long_description_content_type="text/markdown",
)
