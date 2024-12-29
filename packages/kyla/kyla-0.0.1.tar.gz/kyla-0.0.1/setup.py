from setuptools import setup, find_packages

setup(
    name="kyla",  # Nama library di PyPI
    version="0.0.1",  # Versi awal
    author="Firza Aditya ",
    author_email="elbuho1315@gmail.com",
    description="A string utility tool",
    long_description="A string utility tool",
    long_description_content_type="text/plain",
    url="https://github.com/firzaelbuho/pyhelloworld",  # Opsional
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
