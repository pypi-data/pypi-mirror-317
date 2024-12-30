from setuptools import setup, find_packages

setup(
    name='inspyctor',
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        'flake8',
        'bandit',
    ],
    entry_points={
        'console_scripts': [
            'inspyctor = inspyctor.cli:main',
        ],
    },
    description='Command-line tool to review Python code for style and security.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Abhishek Chaudhary',
    author_email='abhishekchaudhary1403@gmail.com',
    url='https://github.com/abhishekchaudharygh/inspyctor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)
