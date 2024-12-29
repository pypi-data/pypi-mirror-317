from setuptools import setup, find_packages

setup(
    name='roadheader',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "setuptools",
        "playwright",
        "playwright_stealth",
    ],
    entry_points={
        'console_scripts': [
        ],
    },
    author='Irid',
    author_email='irid.zzy@gmail.com',
    description='A simple web crawler framework',
    url='https://github.com/iridesc/roadheader',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
