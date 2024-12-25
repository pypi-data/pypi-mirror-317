from setuptools import setup, find_packages

setup(
    name="vuud2",  
    version="0.1.1", 
    packages=find_packages(),         
    classifiers=[  # Классификаторы для PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
)
