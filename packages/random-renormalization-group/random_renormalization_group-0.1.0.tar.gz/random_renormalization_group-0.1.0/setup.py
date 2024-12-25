from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="random_renormalization_group",                
    version="0.1.0",                  
    author="Yang Tian, Pei Sun and Yizhou Xu",    
    description="The package for random renormalization group",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Asuka-Research-Group/Random-renormalization-group",
    packages=find_packages(),      
    classifiers=[            
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",        
    install_requires=[
        "numpy",
        "scipy",
        "faiss-cpu",
        "networkx",
        "datasketch",
        "statsmodels",
    ],
)