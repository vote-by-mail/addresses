from setuptools import setup, find_packages

setup(
  name='addresses',
  package_dir={'': 'osm'},
  packages=find_packages(where='osm'),
  install_requires=['ediblepickle'],
)
