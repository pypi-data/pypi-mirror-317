from setuptools import setup, find_packages

setup(
    name='string_utils_rjl',
    version='1.0.0',
    author='Ruan Jia Lu',
    author_email='your.email@example.com',
    description='A simple package for string operations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://www.example.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'string_utils_rjl=string_utils_rjl.utils:main_function',
        ],
    },
)