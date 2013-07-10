from setuptools import setup

requirements = map(str.strip, open('requirements.txt').readlines())

setup(
  name = 'Dagger',
  classifiers = \
    [
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2',
      'Topic :: Software Development :: Libraries',
    ],
  keywords = 'dagger',
  author = 'Austin Marshall',
  author_email = 'amarshall@groksolutions.com',
  license = 'MIT',
  namespace_packages = ['dagger'],
  packages = ['dagger'],
  entry_points = \
    {
      'console_scripts': \
        [
          'dagger = dagger.cli:main'
        ]
    },
  requires = requirements,
  install_requires = requirements
)