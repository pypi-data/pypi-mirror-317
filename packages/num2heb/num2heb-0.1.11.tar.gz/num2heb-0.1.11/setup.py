from setuptools import setup, find_packages

setup(
    name='num2heb',
    version='0.1.11',
    author='Noam Azoulay',
    author_email='noam@na-systems.com',
    description='A Function to convert a number into words in Hebrew',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/azoulaynoam/num2heb',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # List your package dependencies here
    ],
    include_package_data=True,
)