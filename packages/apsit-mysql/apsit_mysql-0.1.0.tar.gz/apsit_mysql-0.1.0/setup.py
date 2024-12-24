from setuptools import setup, find_packages

setup(
    name="apsit-mysql",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "docker>=6.1.0",
        "click>=8.0.0",
        "platformdirs>=3.0.0"
    ],
    entry_points={
        'console_scripts': [
            'apsit-mysql=apsit_mysql.cli:main',
        ],
    },
    package_data={
        'apsit_mysql': ['docker/*'],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A universal MySQL development environment using Docker",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/apsit-mysql",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)