from setuptools import setup, find_packages

setup(
    name="AutoExpireDB",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary",  # List any other dependencies your package needs
    ],
    author="Siddhanth",
    author_email="thebiryanimonsterr@gmail.comt",
    description="A temporary user management system.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/temp_user_manager",  # Update with the correct URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
