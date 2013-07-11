import os
import sys

from optparse import OptionParser
from subprocess import (
  call,
  PIPE,
  Popen
)

import dagger

parser = OptionParser(usage='%prog dep [PATH] URL REV BRANCH')
parser.add_option('-b', '--branch',
  dest='branch',
  default='CI',
  help='Stable branch name [Default: CI]')
parser.add_option('--commit',
  action='store_true',
  dest='commit',
  default=True)
parser.add_option('--no-commit',
  action='store_false',
  dest='commit',
  default=True)

def handle(options, args):
  """ Specify a dependency """

  if '://' in args[1]:
    path = args.pop(0)
  else:
    path = '.'

  (url, rev, branch) = args[:3]

  with dagger.workingdir(path):
    lastbranch = dagger.getcwdbranch()

    # Checkout working branch
    if call(['git checkout %s' % options.branch], shell=True):
      """ Non-zero return status """
      return

    call(['git log -- dagger.cfg'], shell=True)

    config = dagger.Config()

    """ TODO: update config with dependency details
    """

    if options.commit:
      call(['git add dagger.cfg'], shell=True)

      # Commit
      message = 'dagger deps ' + ' '.join(sys.argv[1:])
      call(['git commit --message="%s"' % message], shell=True)

      # Return to original branch
      call(['git checkout %s' % lastbranch], shell=True)
