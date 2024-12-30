from setuptools import setup, find_packages

setup(
    name='pgss',
    version='0.2.1',
    description='A package to manage session states per page in Streamlit',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Masashi Ueda',
    author_email='',
    url='https://github.com/masashi2ueda/pgss',
    packages=find_packages(),
    install_requires=['streamlit>=1.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7'
)