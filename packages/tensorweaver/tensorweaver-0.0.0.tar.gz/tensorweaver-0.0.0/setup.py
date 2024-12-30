from setuptools import setup, find_packages

setup(
    name="tensorweaver",
    version="0.0.0",
    author="Xiaoquan Kong",
    author_email="u1mail2me@gmail.com",
    description="A package for tensor operations and deep learning (in development)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/howl-anderson/TensorWeaver",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
) 