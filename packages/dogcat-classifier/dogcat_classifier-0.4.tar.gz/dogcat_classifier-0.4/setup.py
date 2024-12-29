from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of the README file for the long description
long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name='dogcat_classifier',
    version='0.4',
    packages=find_packages(),
    include_package_data=True,  # Includes files specified in MANIFEST.in
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
    long_description_content_type='text/markdown',  # Ensures the README is interpreted as markdown
    author='Praneeth-mareddy',
    author_email='saip9091@gmail.com',
    url='https://github.com/praneethmareddy/dogcat_classifier',
    package_data={  # Additional non-code files to include
        "": ["*.md", "*.h5"],  # Includes README.md and model.h5
    },
)
