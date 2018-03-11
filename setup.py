from setuptools import setup, find_packages

import tests
import blockchain


setup(
    name='blockchain',
    version=blockchain.__version__,
    description='Pure python blockchain technology implementation',
    author='Ihor Omelchenko',
    author_email='counter3d@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=['pyramid'],
    test_suite='tests'
)

