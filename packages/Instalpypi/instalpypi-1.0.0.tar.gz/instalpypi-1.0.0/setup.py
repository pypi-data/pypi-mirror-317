from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='Instalpypi',
  version='1.0.0',
  author='Alex',
  author_email='Ls481693@gmail.com',
  description='This is my first module',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Vox0n/projectpypi',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='example python',
  project_urls={
    'Documentation': 'https://github.com/Vox0n/projectpypi'
  },
  python_requires='>=3.7'
)