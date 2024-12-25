from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name="assumption_sheriff",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'statsmodels',
        'lifelines'
    ],
    author="Mohsen Askar",
    author_email="ceaser198511@gmail.com",
    description="A comprehensive statistical assumption checking package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MohsenAskar",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)


