from setuptools import setup, find_packages

setup(
    name='healthpredictor',
    version='0.1.2',
    description='A brief description of your package',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Mohammed Ufraan',
    author_email='kurosen930@gmail.com',
    url='https://github.com/moroii69/proofly-python-package',
    packages=find_packages(),  # Automatically find packages in the current directory
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.18.5',
        'scipy>=1.5.0',
        'typing; python_version<"3.9"',
    ],
    extras_require={
        'dev': [
            'pytest>=3.7',
            'sphinx>=3.0',
        ],
    },
)
