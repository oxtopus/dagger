import os

from contextlib import contextmanager
from fcntl import (
  flock,
  LOCK_EX,
  LOCK_UN
)
from subprocess import (
  PIPE,
  Popen
)


@contextmanager
def workingdir(path):
  """ cd into destination path (obtaining an exclusive lock), yield context,
  cd to original path
  """
  original = os.getcwd()
  with open(os.path.join(path, 'dagger.lock'), 'w') as dagger:
    flock(dagger, LOCK_EX)
    if not os.path.samefile(path, original):
      os.chdir(path)
      yield
      os.chdir(original)
    else:
      yield
    flock(dagger, LOCK_UN)


def getcwdbranch():
  branch = Popen(['git rev-parse --abbrev-ref HEAD'], shell=True, stdout=PIPE)
  return branch.communicate()[0].strip()


def getrevisions(stable, source):
  """ List revisions between stable branch and dagger branch
  """
  revlist = Popen(['git rev-list %s..%s' % (stable, source)], shell=True,
    stdout=PIPE)
  return revlist.communicate()[0].splitlines()

