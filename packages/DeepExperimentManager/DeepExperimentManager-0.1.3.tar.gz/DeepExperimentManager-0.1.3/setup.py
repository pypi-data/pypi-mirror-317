from setuptools import setup, find_packages

setup(
    name='DeepExperimentManager',
    version='0.1.3',
    author='Dexoculus',
    author_email='hyeonbin@hanyang.ac.kr',
    description='A module for training, testing, and managing experiments in PyTorch.',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Dexoculus/PyTorch-Experiment-Manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "tqdm>=4.64.0",
        "pyyaml>=6.0",
        "torch>=2.3.1",
        "torchvision>=0.15.2",
        "numpy>=1.26.4",
        "scikit-learn==1.5.1",
        "matplotlib>=3.8.0",
    ],
)
