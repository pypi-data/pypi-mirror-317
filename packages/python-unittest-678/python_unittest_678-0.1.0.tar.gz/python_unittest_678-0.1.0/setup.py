from setuptools import setup, find_packages

setup(
    name='python-unittest-678',
    version='0.1.0',
    author='igormic',
    description='A Python project for practicing unit testing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').readlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
