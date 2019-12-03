
# NOTE: The package errors can be ignored as some of them 
# cannot be installed due to Operating system environment differences.

# NOTE: The escape key doesn't work well for 
# linux. Find the library allowing me to flexibly modify
# the input.

class _Getch:

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        
        # If the self.impl is unix, then import Unix.
        if (type(self.impl).__name__ == "_GetchUnix"):
            charlist = []
            for i in range(3):
                try:charlist.append(self.impl())
                except:pass
                if charlist[i] not in ["\x1b","\x5b"]:
                    break
            if len(charlist) == 3:
                if charlist[2] == 'A':
                    return 'UP_KEY'
                elif charlist[2] == 'B':
                    return 'DOWN_KEY'
                elif charlist[2] == 'C':
                    return 'RIGHT_KEY'
                elif charlist[2] == 'D':
                    return 'LEFT_KEY'
            elif len(charlist)  == 1:
                if charlist[0] == 'm':
                    return b'\x1b'
                else:
                    return charlist[0].encode()
        
        # Else, import windows one.
        else:
            return self.impl()
    
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
    for i in range(15):
        print(_Getch().__call__())
