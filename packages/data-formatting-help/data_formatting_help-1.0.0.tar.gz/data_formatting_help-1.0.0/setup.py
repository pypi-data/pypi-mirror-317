from setuptools import setup, find_packages

setup(
    name='data_formatting_help',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'bump2version',  # Version bumping
        'pytest',        # Testing
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)