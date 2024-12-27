from setuptools import setup, find_packages

setup(
    name='awspacha',
    version='0.1.4',
    author='Ed Condori',
    author_email='edcondoricc@gmail.com',
    description='Paquete para operaciones con Spark y S3',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/edcondoric/awspacha.git',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'boto3'
    ],
)
