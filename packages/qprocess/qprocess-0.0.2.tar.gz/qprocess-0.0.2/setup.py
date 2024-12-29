from setuptools import setup, find_packages

setup(
    name="qprocess",  # Unique name on PyPI
    version="0.0.2",
    description="A Python library for processing Quantum Chemical program output files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Bogdan Virag",
    author_email="viragbogdan@edu.bme.hu",
    url="https://github.com/fehergandalf/Gaussian.git",  # GitHub or other project URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
            "pandas", "numpy"
    ],
)
