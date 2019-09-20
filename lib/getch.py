# NOTE: Error message appears as one operating system is only compatible to one different package.

class _Getch:
    """Gets a single character from standard input. Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

# TODO: _GetchUnix needs to be modified.
class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        basic_key = msvcrt.getch()
        if basic_key == b"\xe0":
            try:
                return {b"H": "UP_KEY", b"M": "RIGHT_KEY", b"P": "DOWN_KEY", b"K": "LEFT_KEY"}[msvcrt.getch()]
            # pass if the input value is wrong.
            except:
                pass
        else:
            return basic_key

# Reference: Yoo, D. (2002). getch()-like unbuffered character reading from stdin on both 
#   windows and unix (Python recipe) [Source code].
#   Retreived from http://code.activestate.com/recipes/134892/

if __name__ == "__main__":
    for i in range(5):
        print(_Getch().__call__())
