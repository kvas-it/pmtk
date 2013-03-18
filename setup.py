from setuptools import setup
from setuptools import find_packages

with open("README.txt") as f:
    README = f.read()

with open("CHANGES.txt") as f:
    CHANGES = f.read()

setup(name='ppl',
      version='1.0',
      packages=find_packages(),
      description=("Project Plan Language toolkit"),
      long_description=README + '\n' + CHANGES,
      author='Vasily Kuznetsov',
      author_email='kvas.it@gmail.com',
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools'],
      keywords='Project Management Toolkit',
      url='https://github.com/kvas-it/pmtk',
      namespace_packages=['pmtk'])
