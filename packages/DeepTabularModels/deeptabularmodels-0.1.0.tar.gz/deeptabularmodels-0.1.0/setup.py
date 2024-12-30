from setuptools import setup, find_packages

setup(
    name="DeepTabularModels",  
    version="0.1.0", 
    description="Deep learning for tabular data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  
    author="Ali Haidar Ahmad", 
    author_email="ali.h.ahmad001@gmail.com",   
    url="https://github.com/AliHaiderAhmad001/deep-tabular.git",  
    packages=find_packages(),
    install_requires=[ 
    ],
    classifiers=[        
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  
)

