from setuptools import setup, find_packages

setup(
    name="airfoil-tools",
    version="1.0.1",
    description="A python library for working with airfoil shapes, including NACA airfoils.",
    author="Josh",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=["numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)