# setup.py

from setuptools import setup, find_packages

# Read the contents of README.md
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='delivery-person',  # Package name
    version='0.1.0',
    author='Faditech',
    author_email='issakafadil@gmail.com',
    description='A package to detect delivery persons in images using a fine-tuned ResNet-50 model.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/issakafadil/delivery-person',  # Replace with your repository URL
    packages=find_packages(),
    install_requires=[
        'torch>=1.7.1',
        'torchvision>=0.8.2',
        'Pillow>=8.0.1',
        'numpy>=1.19.2',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
