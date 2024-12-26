#https://www.youtube.com/watch?v=5KEObONUkik&t=132s


from setuptools import setup, find_packages

# Define the setup for the package
setup(
    name="table_partitionare",  
    version="1.0.0",  
    author="Ehsan S.Mohammadi",  
    author_email="ehsannsam@gmail.com", 
    description="A library for partitioning PostgreSQL tables",  # Short description of your package
    long_description=open("README.md").read(),  # Long description from README.md
    long_description_content_type="text/markdown",  # The format of the long description
    url="https://github.com/ehsansam90/TablePartitionare",  # URL to your package's repository
    package_dir={"":"app"},
    packages=find_packages(where="app"),  # Automatically find all packages in the project
    install_requires=[  # List of dependencies required by the package
    "greenlet==3.1.1",  # Greenlet library for concurrency support (used with SQLAlchemy)
    "psycopg2-binary==2.9.10",  # PostgreSQL adapter for Python
    "python-dotenv==1.0.1",  # To load environment variables from .env file
    "SQLAlchemy==2.0.36",  # SQLAlchemy for interacting with PostgreSQL
],
    classifiers=[  # Classifiers to help users find your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify the minimum Python version
    zip_safe=False,  # Don't install as a .egg, ensuring the package can be used directly

    
)
