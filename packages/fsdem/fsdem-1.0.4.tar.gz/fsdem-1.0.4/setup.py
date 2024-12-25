from setuptools import setup, find_packages

setup(
    name='fsdem',
    version='1.0.4',
    author='Muhammad Rajabinasab',
    author_email='muhammad.rajabinasab@outlook.com',
    description='Feature Selection Dynamic Evaluation Metric',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mrajabinasab/FSDEM-Feature-Selection-Dynamic-Evaluation-Metric',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)