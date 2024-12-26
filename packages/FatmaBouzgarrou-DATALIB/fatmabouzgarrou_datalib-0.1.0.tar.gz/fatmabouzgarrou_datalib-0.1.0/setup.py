from setuptools import setup, find_packages

try:
    with open('README.md', 'r') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = 'A simple data manipulation and analysis library (README not found)'

setup(
    name="FatmaBouzgarrou-DATALIB", 
    version="0.1.0",  
    description="A simple data manipulation and analysis library",
    long_description=long_description,
    long_description_content_type='text/markdown',  
    author="Fatma Bouzgarrou",  
    author_email="fatmabouzgarrou6@gmail.com",  
    packages=find_packages(where='src'), 
    package_dir={'': 'src'},  
    install_requires=[  
        "numpy",
        "pandas",
        "matplotlib",
        "scikit-learn",
    ],
    extras_require={  
        "dev": ["pytest", "sphinx", "tox"],
    },
    test_suite='tests',  
    python_requires='>=3.7',  
    classifiers=[  
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
