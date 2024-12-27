from setuptools import setup, find_packages

setup(
    name="numap",
    version="0.1.11",
    description="Generalizable UMAP Implementation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nir Ben-Ari",
    author_email="nirnirba@gmail.com",
    url="https://github.com/TheNirnir/NUMAP",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "pytorch-lightning>=2.5.0",
        "pynndescent>=0.5.13",
        "umap-learn>=0.5.7",
        "dill>=0.3.9",
        "grease-embeddings>=0.1.1",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
)
