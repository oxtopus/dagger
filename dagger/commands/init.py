import os
import sys

from optparse import OptionParser
from subprocess import call

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


def handle(options, args):
  """ Initialize a project """

  try:
    path = args.pop(0)
  except IndexError:
    path = '.'

  with dagger.workingdir(path):
    result = call(['git show-ref --verify refs/heads/%s' % options.branch], shell=True)
    if result:
      # CI branch does not exist... Create it
      lastbranch = dagger.getcwdbranch()

      # Orphaned checkout
      call(['git checkout --orphan %s' % options.branch], shell=True)
      call(['git rm -rf .'], shell=True)

      # Write dagger config...
      conf = dagger.Config()
      conf.set('dagger', 'tracking', lastbranch)
      conf.set('dagger', 'script', '')
      conf.save()

      call(['git add dagger.cfg'], shell=True)

      # Commit
      message = 'dagger init ' + ' '.join(sys.argv[1:])
      call(['git commit --message="%s"' % message], shell=True)

      # Return to original branch
      call(['git checkout %s' % lastbranch], shell=True)

      print options.branch, 'branch created with initial dagger config.\n'
      print 'Next step: Checkout', options.branch, 'and configure dagger.'

    else:
      print 'Nothing to do.'
