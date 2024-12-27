from setuptools import setup, find_packages

setup(
    name='dreemui',  # PyPI package name
    version='0.1.0',  # Initial version
    packages=find_packages(),  # Automatically find sub-packages
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    description='A simple library to scrape and download websites',
    long_description=open('README.md').read(),  # README file content
    long_description_content_type='text/markdown',
    author='Dhrvu Ahir',
    author_email='incnogeto@gmail.com',
    url='https://github.com/yourusername/dreemui',  # Replace with your GitHub repository
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
