from setuptools import setup, find_packages

setup(
    name='Fkillera',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple package for Fkillera',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://www.example.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # Add any dependencies here
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'Fkillera=Fkillera.operations:main_function',
        ],
    },
)
