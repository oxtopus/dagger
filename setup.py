import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


requirements = map(str.strip, open('requirements.txt').readlines())

class PyTest(TestCommand):
  def finalize_options(self):
    TestCommand.finalize_options(self)
    self.test_args = []
    self.test_suite = True
  def run_tests(self):
    import pytest
    errno = pytest.main(self.test_args)
    sys.exit(errno)

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
  install_requires = requirements,
  tests_require = ['pytest'],
  cmdclass = \
    {
      'test': PyTest
    },
)