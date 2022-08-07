from setuptools import setup, find_packages

setup(
    name='evtol_crawler',
    version='0.0.1',
    license='MIT',
    author="Benyamin Kosari",
    author_email='benyaminusc@gmail.com',
    packages=find_packages('source'),
    package_dir={'': 'source'},
    url='https://github.com/benyaminkosari/evtol_crawler',
    keywords='evtol crawler',
    install_requires=[
          'requests',
          'bs4',
      ],
)
