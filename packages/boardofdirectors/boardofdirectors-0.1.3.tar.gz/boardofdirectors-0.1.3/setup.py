from setuptools import setup, find_packages

setup(
    name="boardofdirectors",  # The name of your package
    version="0.1.3",  # Package version
    packages=find_packages(),  # Automatically find Python packages in the directory
    install_requires=[],
    description="A package for machine learning models and preprocessing tools",  # Brief description of your package
    author="Pseudonym",  # Use your name or a pseudonym
    author_email="audiodramaa@gmail.com",  # Use an anonymous email if you want to stay anonymous
    classifiers=[  # Optional: Categorization for your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # You can use other licenses if preferred
        "Operating System :: OS Independent",  # Operating system compatibility
    ],
    python_requires='>=3.6',  # Ensure the package is compatible with Python 3.6+
)
