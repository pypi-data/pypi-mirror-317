from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of the README file for the long description
long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name='dogcat_classifier',
    version='0.6',
    packages=find_packages(),
    include_package_data=True,  # Ensures files listed in MANIFEST.in are included
    install_requires=[
        'tensorflow',
        'tensorflow_hub',
        'pillow',
        'numpy',
        'matplotlib',
        'scikit-learn',
        'opencv-python',
    ],
    description='This project focuses on creating a machine learning model that classifies images of dogs and cats. The model is encapsulated within a Python package, making it easy to install and use. The package employs TensorFlow for model training and inference, while OpenCV and Pillow are utilized for image processing. It is distributed via PyPI (Python Package Index).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Praneeth_mareddy',
    author_email='saip9091@gmail.com',
    url='https://github.com/praneethmareddy/dogcat_classifier',
    package_data={
        'dogcat_classifier': ['model.h5'],  # Ensure model.h5 is included in the package
    },
)
