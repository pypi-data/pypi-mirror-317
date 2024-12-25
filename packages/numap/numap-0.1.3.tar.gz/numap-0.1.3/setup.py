from setuptools import setup, find_packages

setup(
    name="numap",
    version="0.1.3",
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
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
)
