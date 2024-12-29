from setuptools import setup, find_packages

setup(
    name="alexx",
    version="0.2.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple CLI tool example",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'alexx=alexx.main:main',  # 'command-name=package.module:function'
        ],
    },
)