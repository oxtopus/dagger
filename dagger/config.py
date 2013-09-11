from ConfigParser import ConfigParser

class Config(ConfigParser):
  def __init__(self, *args, **kwargs):
    ConfigParser.__init__(self, *args, **kwargs)

    self.read(['dagger.cfg'])

    if not self.has_section('dagger'):
      self.add_section('dagger')

    if not self.has_option('dagger', 'tracking'):
      self.set('dagger', 'tracking', '')

  def save(self):
    with open('dagger.cfg', 'w') as outp:
      self.write(outp)