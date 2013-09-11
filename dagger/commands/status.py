import sys

from optparse import OptionParser
from subprocess import call

import dagger

parser = OptionParser(usage='%%prog %s [PATH]' % __name__.rpartition('.')[2])
parser.add_option('-b', '--branch',
  dest='branch',
  default='CI',
  help='Stable branch name [Default: CI]')


def handle(options, args):
  """ Every dagger has a handle! """

  try:
    path = args.pop(0)
  except IndexError:
    path = '.'

  with dagger.workingdir(path):
    lastbranch = dagger.getcwdbranch()

    # Checkout working branch
    if call(['git checkout %s' % options.branch], shell=True):
      print "Stable branch", options.branch, "cannot be found, you can " \
        "create one with `dagger init`.  See `dagger help` for additional " \
        "details."
      return

    config = dagger.Config()
    tracking = config.get('dagger', 'tracking')
    revisions = dagger.getrevisions(options.branch, tracking)
    print options.branch, 'is', len(revisions), 'revisions behind', tracking

    # Return to original branch
    call(['git checkout %s' % lastbranch], shell=True)