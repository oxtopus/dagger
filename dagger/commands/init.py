import os
import sys

from contextlib import contextmanager
from fcntl import (
  flock,
  LOCK_EX,
  LOCK_UN
)
from optparse import OptionParser
from subprocess import (
  call,
  PIPE,
  Popen
)
from StringIO import StringIO
from tempfile import TemporaryFile

import dagger

parser = OptionParser(usage='%prog init [PATH]')
parser.add_option('-b', '--branch',
  dest='branch',
  default='CI',
  help='Stable branch name [Default: CI]')
parser.add_option('-d', '--dependencies',
  dest='dependencies',
  metavar='FILE',
  help='Project dependencies')
parser.add_option('--dry-run',
  dest='dryrun',
  action='store_true',
  default=False,
  help='Do not make changes.')


@contextmanager
def workingdir(path):
  """ cd into destination path (obtaining an exclusive lock), yield context,
  cd to original path
  """
  original = os.getcwd()
  with open(os.path.join(path, 'dagger'), 'w') as dagger:
    flock(dagger, LOCK_EX)
    if not os.path.samefile(path, original):
      os.chdir(path)
      yield
      os.chdir(original)
    else:
      yield
    flock(dagger, LOCK_UN)

def handle(options, args):
  """ Every dagger has a handle! """

  try:
    path = args.pop(0)
  except IndexError:
    path = '.'

  with workingdir(path):
    result = call(['git show-ref --verify refs/heads/%s' % options.branch], shell=True)
    if result:
      # CI branch does not exist... Create it
      branch = Popen(['git rev-parse --abbrev-ref HEAD'], shell=True,
        stdout=PIPE)
      lastbranch = branch.communicate()[0].strip()

      # Orphaned checkout
      call(['git checkout --orphan %s' % options.branch], shell=True)
      call(['git rm -rf .'], shell=True)

      # Write dependencies...
      with open('dependencies.txt', 'w') as outp:
        pass

      call(['git add dependencies.txt'], shell=True)

      # Commit
      message = 'dagger init ' + ' '.join(sys.argv[1:])
      call(['git commit --message="%s"' % message], shell=True)

      # Return to original branch
      call(['git checkout %s' % lastbranch], shell=True)

      print options.branch, 'branch created with empty dependencies.txt\n'
      print 'Next step: Checkout', options.branch, 'update dependencies'

