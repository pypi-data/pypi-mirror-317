# Overview
This is the code implementation of the random renormalization group presented in the paper entitled as "Fast renormalizing the structures and dynamics of ultra-large systems via random renormalization group". 

# Instructions
example.py can be run directly over simulated data.  To run the codes with real data, one only needs to change the input of the function Renormalization_Flow. We refer to “Fast_renormalizing_the_structures_and_dynamics_of_ultra_large_systems_via_random_renormalization_group_SM_.pdf” for detailed descriptions and usages of other functions.

# System requirements
## Hardware requirements
Our codes only require a modest size computer with enough RAM to support in-memory operations. All the computations are implemented in a CPU environment. To date, our codes have been implemented in a 256GB environment with two Intel Xeon Gold 5218 processors and a 32GB environment with a Intel Core i7-8750H CPU for testing.

## OS requirements
Our codes have been tested on the following system:
+ windows 10

## Python dependencies
Our codes mainly depends on following packages:
```python
numpy
scipy
faiss
networkx
datasketch
statsmodels
```

# Installation guide:
```python
pip install random_renormalization_group
```

# License
This project is covered under the **MIT License**.