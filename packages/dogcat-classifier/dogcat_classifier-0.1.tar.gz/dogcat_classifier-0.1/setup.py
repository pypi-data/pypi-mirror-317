from setuptools import setup, find_packages

setup(
    name='dogcat_classifier',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'tensorflow',
        'pillow',
        'numpy',
        'matplotlib',
        'scikit-learn',
        'opencv-python',
    ],
    description='A package for classifying Dog vs Cat images using a deep learning model.',
    author='Your Name',
    author_email='your-email@example.com',
    url='https://github.com/yourusername/dogcat_classifier',  # Your project URL
)
