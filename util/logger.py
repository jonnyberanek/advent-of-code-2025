from util import context

class Logger():
  def t(self, *args, **kwargs):
    """Test level"""
    if not context.is_test:
      return
    print(*args, **kwargs)

  def v(self, *args, **kwargs):
    """Verbose (real data) level"""
    print(*args, **kwargs)

logger = Logger()