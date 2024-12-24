from setuptools import setup, find_packages

setup(
    name='AutoExpireDB',
    version='2.0.0',
    author="Siddhanth",
    author_email="thebiryanimonsterr@gmail.com",
    description='A library for automatically expiring database users and password entries.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mafiaguy/AutoExpireDB',
    license='MIT',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "psycopg2-binary",
    ],
)
