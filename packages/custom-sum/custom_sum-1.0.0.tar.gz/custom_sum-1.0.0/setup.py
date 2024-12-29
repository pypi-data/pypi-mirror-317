from setuptools import setup, find_packages

setup(
    name="custom-sum",  # Package name
    version="1.0.0",  # Package version
    author="Khalid Sulaiman Al-Mulaify",  # Your name
    author_email="khalidmfy@gmail.com",  # Your email
    description="A Python package for summation with filtering and string concatenation.",  # Short description
    packages=find_packages(),  # Automatically find and include your packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # License type
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)
