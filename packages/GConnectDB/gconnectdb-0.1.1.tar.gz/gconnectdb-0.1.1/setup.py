from setuptools import setup, find_packages

setup(
    name="GConnectDB",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python",
        "pyotp",
    ],
    author="Jagadeesan",
    author_email="jagadeesan.murugesan@saviynt.com",
    description="A library to connect to MySQL using SSH tunnel and Google Authentication",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jagadeesan.murugesan/GConnectDB",
    classifiers=[  # PyPI classifiers
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version
)