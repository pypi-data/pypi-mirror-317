# setup.py

from setuptools import setup, find_packages

setup(
    name='image_processing_toolkit_wwy',
    version='1.0.0',
    author='202313093029_.wwy',
    author_email='202313093029@cuc.edu.cn',
    description='A simple toolkit for image processing',
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
        'Pillow',  # PIL fork for image processing
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'image_processing_toolkit=image_processing_toolkit.operations:main',
        ],
    },
)
