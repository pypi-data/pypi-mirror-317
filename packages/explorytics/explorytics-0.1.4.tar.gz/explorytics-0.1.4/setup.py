from setuptools import setup, find_packages

setup(
    name="explorytics",
    version="0.1.4",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "plotly>=5.0.0",
        "scipy>=1.7.0",
    ],
    python_requires=">=3.8",
    author="Mohit Mahajan",
    author_email="mohitmahajan3715@gmail.com",
    description="A comprehensive Python library for Exploratory Data Analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mohitmahajan095/explorytics",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)