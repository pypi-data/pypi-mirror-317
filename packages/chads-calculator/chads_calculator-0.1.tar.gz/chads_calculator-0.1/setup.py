from setuptools import setup, find_packages

setup(
    name='chads_calculator',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    test_suite='tests',
    author="Vlad_Chad",
    author_email="3336096509@qq.com",
    description="A simple calculator library for basic arithmetic operations.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
