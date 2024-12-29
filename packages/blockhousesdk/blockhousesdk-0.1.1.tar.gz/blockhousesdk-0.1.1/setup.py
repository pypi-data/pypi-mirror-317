from setuptools import setup, find_packages

setup(
    name='blockhousesdk',
    version='0.1.1',
    author='Zubair',
    author_email='zubair.flexlab@gmail.com',
    description='A Python SDK for Blockhouse to transfer files',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'boto3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)