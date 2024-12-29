from setuptools import setup, find_packages

setup(
    name='dogcat_classifier',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
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
    author='Praneeth-mareddy',
    author_email='saip9091@gmail.com',
    url='https://github.com/praneethmareddy/dogcat_classifier',
)
