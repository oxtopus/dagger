import os
import sys

from optparse import OptionParser
from subprocess import (
  call,
  PIPE,
  Popen
)
from StringIO import StringIO
from tempfile import TemporaryFile

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
  """ Every dagger has a handle! """

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

    call(['git log -- dependencies.txt'], shell=True)

    with open('dependencies.txt', 'r') as outp:
      for line in outp:
        dep = line.strip().split(' ')
        if dep[0] == url and branch == dep[2]:
          # Return to original branch
          call(['git checkout %s' % lastbranch], shell=True)
          return

    with open('dependencies.txt', 'a') as outp:
      outp.write(' '.join(args) + '\n')

    if options.commit:
      call(['git add dependencies.txt'], shell=True)

      # Commit
      message = 'dagger deps ' + ' '.join(sys.argv[1:])
      call(['git commit --message="%s"' % message], shell=True)

      # Return to original branch
      call(['git checkout %s' % lastbranch], shell=True)


