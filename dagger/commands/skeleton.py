import sys

from optparse import OptionParser

import dagger

parser = OptionParser(usage='%%prog %s [PATH]' % __name__.rpartition('.')[2])

def handle(options, args):
  """ Every dagger has a handle! """

  try:
    path = args.pop(0)
  except IndexError:
    path = '.'

  with dagger.workingdir(path):
    pass