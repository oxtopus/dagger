import sys
from optparse import OptionParser

import commands



availableCommands = \
  __import__('dagger.commands', globals(), locals(), ['*'])

commands = dict([
    (cmd, getattr(availableCommands, cmd))
    for cmd in availableCommands.__all__
  ])

usage = "%prog [command] [options]\n\n" \
        "Available commands:\n"

for command in commands:
  usage += "\n    " + command

parser = OptionParser(usage=usage)


def handle(options, args):
  parser.print_help()


def main():
  try:
    subcommand = sys.argv.pop(1)
  except IndexError:
    print parser.print_help()
    sys.exit()

  submodule = commands.get(subcommand, sys.modules[__name__])

  (options, args) = submodule.parser.parse_args(sys.argv[1:])

  submodule.handle(options, args)


if __name__ == '__main__':
  main()