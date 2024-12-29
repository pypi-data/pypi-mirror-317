from setuptools import setup, find_packages

setup(
    name="line-integral-convolutions",
    version="1.0.0",
    description="A script showcasing my implementation for computing line integral convolution.",
    author="Neco Kriel",
    author_email="neco.kriel@anu.edu.au",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["numpy", "matplotlib", "scipy", "numba", "scikit-image"],
)
