from setuptools import setup, find_packages

setup(
    name="AutoExpireDB",
    version="0.1.0",
    package_dir={"": "src"},  # This tells setuptools to look in the 'src' directory for packages
    packages=find_packages(where="src"),  # Look for packages within the 'src' directory
    install_requires=[
        "psycopg2-binary",  # Add or modify based on your dependencies
    ],
    author="Siddhanth",
    author_email="thebiryanimonsterr@gmail.com",
    description="A library for automatically expiring database entries.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/autoexpiredb",  # Update with your GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
